import json
import platform
import subprocess
import threading
import time
from typing import Dict, List, Optional, Union

import psutil
import wandb
from wandb import util
from wandb.vendor.pynvml import pynvml

from wandb.sdk.internal import ipu
from wandb.sdk.internal import tpu
from wandb.sdk.internal.settings_static import SettingsStatic
from wandb.sdk.interface.interface_queue import InterfaceQueue
from wandb.sdk.lib import telemetry


GPUHandle = object
SamplerDict = Dict[str, List[float]]
StatsDict = Dict[str, Union[float, Dict[str, float]]]


# TODO: hard coded max watts as 16.5, found this number in the SMC list.
# Eventually we can have the apple_gpu_stats binary query for this.
M1_MAX_POWER_WATTS = 16.5


def gpu_in_use_by_this_process(gpu_handle: GPUHandle, pid: int) -> bool:
    if not psutil:
        return False

    try:
        base_process = psutil.Process(pid=pid)
    except psutil.NoSuchProcess:
        # do not report any gpu metrics if the base process cant be found
        return False

    our_processes = base_process.children(recursive=True)
    our_processes.append(base_process)

    our_pids = {process.pid for process in our_processes}

    compute_pids = {
        process.pid
        for process in pynvml.nvmlDeviceGetComputeRunningProcesses(gpu_handle)
    }
    graphics_pids = {
        process.pid
        for process in pynvml.nvmlDeviceGetGraphicsRunningProcesses(gpu_handle)
    }

    pids_using_device = compute_pids | graphics_pids

    return len(pids_using_device & our_pids) > 0


class WandbSystemStats:

    _pid: int
    _interface: InterfaceQueue
    sampler: SamplerDict
    samples: int
    _settings: SettingsStatic
    _thread: Optional[threading.Thread]
    gpu_count: int

    def __init__(self, settings: SettingsStatic, interface: InterfaceQueue) -> None:
        try:
            pynvml.nvmlInit()
            self.gpu_count = pynvml.nvmlDeviceGetCount()
        except Exception:
            self.gpu_count = 0
        self.refresh_apple_gpu = False
        # self.run = run
        self._settings = settings
        self._pid = settings._stats_pid
        self._interface = interface
        self.sampler = {}
        self.samples = 0
        self._shutdown = False
        self._telem = telemetry.TelemetryRecord()
        if psutil:
            net = psutil.net_io_counters()
            self.network_init = {"sent": net.bytes_sent, "recv": net.bytes_recv}
        else:
            wandb.termlog(
                "psutil not installed, only GPU stats will be reported.  Install with pip install psutil"
            )
        self._thread = None
        self._tpu_profiler = None

        if tpu.is_tpu_available():
            try:
                self._tpu_profiler = tpu.get_profiler()
            except Exception as e:
                wandb.termlog("Error initializing TPUProfiler: " + str(e))

        self._ipu_profiler = None

        if ipu.is_ipu_available():
            try:
                self._ipu_profiler = ipu.IPUProfiler(self._pid)
            except Exception as e:
                wandb.termlog("Error initializing IPUProfiler: " + str(e))

    def start(self) -> None:
        if self._thread is None:
            self._shutdown = False
            self._thread = threading.Thread(target=self._thread_body)
            self._thread.name = "StatsThr"
            self._thread.daemon = True
        if not self._thread.is_alive():
            self._thread.start()
        if self._tpu_profiler:
            self._tpu_profiler.start()

    @property
    def proc(self) -> psutil.Process:
        return psutil.Process(pid=self._pid)

    @property
    def sample_rate_seconds(self) -> float:
        """Sample system stats every this many seconds, defaults to 2, min is 0.5"""
        sample_rate = self._settings._stats_sample_rate_seconds
        # TODO: handle self._api.dynamic_settings["system_sample_seconds"]
        return max(0.5, sample_rate)

    @property
    def samples_to_average(self) -> int:
        """The number of samples to average before pushing, defaults to 15 valid range (2:30)"""
        samples = self._settings._stats_samples_to_average
        # TODO: handle self._api.dynamic_settings["system_samples"]
        return min(30, max(2, samples))

    def _thread_body(self) -> None:
        while True:
            stats = self.stats()
            for stat, value in stats.items():
                if isinstance(value, (int, float)):
                    self.sampler[stat] = self.sampler.get(stat, [])
                    self.sampler[stat].append(value)
            self.samples += 1
            if self._shutdown or self.samples >= self.samples_to_average:
                self.flush()
                if self._shutdown:
                    break
            seconds = 0.0
            while seconds < self.sample_rate_seconds:
                time.sleep(0.1)
                seconds += 0.1
                if self._shutdown:
                    self.flush()
                    return

    def shutdown(self) -> None:
        self._shutdown = True
        try:
            if self._thread is not None:
                self._thread.join()
        finally:
            self._thread = None
        if self._tpu_profiler:
            self._tpu_profiler.stop()

    def flush(self) -> None:
        stats = self.stats()
        for stat, value in stats.items():
            # TODO: a bit hacky, we assume all numbers should be averaged.  If you want
            # max for a stat, you must put it in a sub key, like ["network"]["sent"]
            if isinstance(value, (float, int)):
                # samples = list(self.sampler.get(stat, [stats[stat]]))
                samples = list(self.sampler.get(stat, [value]))
                stats[stat] = round(sum(samples) / len(samples), 2)
        # self.run.events.track("system", stats, _wandb=True)
        if self._interface:
            self._interface.publish_stats(stats)
        self.samples = 0
        self.sampler = {}

    def stats(self) -> StatsDict:
        stats: StatsDict = {}
        try:
            for i in range(0, self.gpu_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                try:
                    utilz = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
                    temp = pynvml.nvmlDeviceGetTemperature(
                        handle, pynvml.NVML_TEMPERATURE_GPU
                    )
                    name = pynvml.nvmlDeviceGetName(handle)
                    name = name.decode("utf-8", errors='ignore')
                    in_use_by_us = gpu_in_use_by_this_process(handle, pid=self._pid)

                    stats["gpu.{}.{}".format(i, "gpu")] = utilz.gpu
                    stats["gpu.{}.{}".format(i, "memory")] = utilz.memory
                    stats["gpu.{}.{}".format(i, "memoryAllocated")] = (
                        memory.used / float(memory.total)
                    ) * 100
                    stats["gpu.{}.{}".format(i, "temp")] = temp
                    stats["gpu.{}.{}".format(i, "name")] = name

                    if in_use_by_us:
                        stats["gpu.process.{}.{}".format(i, "gpu")] = utilz.gpu
                        stats["gpu.process.{}.{}".format(i, "memory")] = utilz.memory
                        stats["gpu.process.{}.{}".format(i, "memoryAllocated")] = (
                            memory.used / float(memory.total)
                        ) * 100
                        stats["gpu.process.{}.{}".format(i, "temp")] = temp

                        # Some GPUs don't provide information about power usage
                    try:
                        power_watts = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
                        power_capacity_watts = (
                            pynvml.nvmlDeviceGetEnforcedPowerLimit(handle) / 1000.0
                        )
                        power_usage = (power_watts / power_capacity_watts) * 100

                        stats["gpu.{}.{}".format(i, "powerWatts")] = power_watts
                        stats["gpu.{}.{}".format(i, "powerPercent")] = power_usage

                        if in_use_by_us:
                            stats["gpu.process.{}.{}".format(i, "powerWatts")] = power_watts
                            stats[
                                "gpu.process.{}.{}".format(i, "powerPercent")
                            ] = power_usage

                    except pynvml.NVMLError:
                        pass

                except pynvml.NVMLError:
                    pass
        except Exception as e:
            pass

        # On Apple M1 systems let's look for the gpu
        if (
            platform.system() == "Darwin"
            and platform.processor() == "arm"
            and self.refresh_apple_gpu
        ):
            try:
                out = subprocess.check_output([util.apple_gpu_stats_binary(), "--json"])
                m1_stats = json.loads(out.split(b"\n")[0])
                stats["gpu.0.memory"] = m1_stats["mem_used"] / float(m1_stats["utilization"]/100)
                stats["gpu.0.gpu"] = m1_stats["utilization"]
                stats["gpu.0.memoryAllocated"] = m1_stats["mem_used"]
                stats["gpu.0.temp"] = m1_stats["temperature"]
                stats["gpu.0.powerWatts"] = m1_stats["power"]
                stats["gpu.0.powerPercent"] = (
                    m1_stats["power"] / M1_MAX_POWER_WATTS
                ) * 100
                # TODO: this stat could be useful eventually, it was consistently
                # 0 in my experimentation and requires a frontend change
                # so leaving it out for now.
                # stats["gpu.0.cpuWaitMs"] = m1_stats["cpu_wait_ms"]

                if self._interface and not self._telem.env.m1_gpu:
                    self._telem.env.m1_gpu = True
                    self._interface._publish_telemetry(self._telem)

            except (OSError, ValueError, TypeError, subprocess.CalledProcessError) as e:
                wandb.termwarn(f"GPU stats error {e}")
                pass

        if psutil:
            net = psutil.net_io_counters()
            sysmem = psutil.virtual_memory()
            stats["cpu"] = psutil.cpu_percent()
            stats["memory"] = sysmem.percent
            stats["network"] = {
                "sent": net.bytes_sent - self.network_init["sent"],
                "recv": net.bytes_recv - self.network_init["recv"],
            }
            # TODO: maybe show other partitions, will likely need user to configure
            stats["disk"] = psutil.disk_usage("/").percent
            stats["proc.memory.availableMB"] = sysmem.available / 1048576.0
            try:
                stats["proc.memory.rssMB"] = self.proc.memory_info().rss / 1048576.0
                stats["proc.memory.percent"] = self.proc.memory_percent()
                stats["proc.cpu.threads"] = self.proc.num_threads()
            except psutil.NoSuchProcess:
                pass
        if self._tpu_profiler:
            tpu_utilization = self._tpu_profiler.get_tpu_utilization()
            if tpu_utilization is not None:
                stats["tpu"] = tpu_utilization

        if self._ipu_profiler:
            stats.update(self._ipu_profiler.get_metrics())
        return stats
