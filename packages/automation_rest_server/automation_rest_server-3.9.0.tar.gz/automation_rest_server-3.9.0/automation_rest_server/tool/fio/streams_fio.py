import multiprocessing
import time
import re
import json
import os
import subprocess
import psutil
import numpy as np
from datetime import datetime, timezone, timedelta
from test_framework.performance_database import decorate_collect_summary_result
from utils import log
from .fio import Fio


class StreamsFio(Fio):
    def __init__(self):
        super().__init__()
        self.msl = 4
        self.fio_process_num = self.msl

    def directives_receive(self, dev_name="/dev/nvme0", dtype=1, doper=1) -> bytes:
        cmd = f"nvme dir-receive {dev_name} --dir-type {dtype} --dir-oper {doper} -b"
        popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=False)
        popen.wait()
        return popen.stdout.read()

    def identify_ns(self, dev_name="/dev/nvme0n1") -> bytes:
        cmd = f"nvme id-ns {dev_name} -b"
        popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=False)
        popen.wait()
        if popen.returncode != 0:
            log.ERR(f"command return: {popen.returncode}")
        return popen.stdout.read()

    def set_streams(self, streams_lbas=0, streams_count=0, streams_mode=0, block_dev="/dev/nvme0n1"):
        log.INFO("Set Streams: streams_lbas: %s, streams_count: %s, streams_mode: %s",
                 streams_lbas, streams_count, streams_mode)
        cmd = f"python3 Utility/driver_set_streams.py -c {streams_count} " \
              f"-m {streams_mode} " \
              f"-l {streams_lbas} " \
              f"-d {block_dev}"
        log.INFO(f"command: {cmd}")
        popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=True)
        popen.wait()
        if popen.returncode != 0:
            log.ERR(f"command return: {popen.returncode}")
        return popen.returncode

    def bandwidth_monitor(self, disk_name="nvme0n1", time_to_monitor=0):
        if time_to_monitor is None:
            time_to_monitor = 0
        disk_name = disk_name.split(r"/")[-1]
        log.INFO("monitor %s", disk_name)
        start_listening = time.perf_counter() if time_to_monitor > 0 else 0
        current_time = time.perf_counter() if time_to_monitor > 0 else 0
        disk_io_counters = psutil.disk_io_counters(perdisk=True)[disk_name]
        last_read_bytes = disk_io_counters.read_bytes
        last_write_bytes = disk_io_counters.write_bytes
        time.sleep(1)
        while (current_time - start_listening) <= time_to_monitor:
            current_time = time.perf_counter() if time_to_monitor > 0 else 0
        # for i in range(time_to_monitor):
            disk_io_counters = psutil.disk_io_counters(perdisk=True)[disk_name]
            read_bytes = disk_io_counters.read_bytes
            write_bytes = disk_io_counters.write_bytes
            read_speed = read_bytes - last_read_bytes
            write_speed = write_bytes - last_write_bytes
            log.INFO(f"[R bw: {read_speed / 1024 / 1024:.2f} MB/s]"
                     f"[W bw: {write_speed / 1024 / 1024:.2f} MB/s]")
            last_read_bytes = read_bytes
            last_write_bytes = write_bytes
            time.sleep(1)

    def call_start_fio(self, cmd):
        log.INFO(cmd)
        status = subprocess.call(cmd, shell=True)
        return status

    def seq_write_background(self, parameters):
        log.INFO(f"seq_write_background: {parameters}")
        blocksize = parameters["background_fio"].get("blocksize")
        iodepth = parameters["background_fio"].get("iodepth")
        numjobs = parameters["background_fio"].get("numjobs")
        bs = blocksize if blocksize is not None else "256k"
        log.INFO(f"seq_write_background: bs {bs}")
        iodph = iodepth if iodepth is not None else "32"
        log.INFO(f"seq_write_background: iodepth {iodph}")
        njbs = numjobs if numjobs is not None else "1"
        log.INFO(f"seq_write_background: numjobs {njbs}")
        size = "100%"
        if parameters["size"]:
            size = f"{parameters['size']}%"
        elif parameters["background_fio"]["size"]:
            size = parameters["background_fio"]["size"]
        elif parameters["fio"]["size"]:
            size = parameters["fio"]["size"]
        seq_write_parameters = {
            "rw": "write",
            "ioengine": parameters["fio"]["ioengine"],
            "filename": parameters["fio"]["filename"],
            "continue_on_error": "all",
            "name": "seq_write_background",
            "blocksize": bs,
            "iodepth": iodph,
            "numjobs": njbs,
            "rwmixread": "0",
            "size": size,
            "runtime": str(int(parameters["fio"]["runtime"]) + 20),
        }
        log.INFO(seq_write_parameters)
        background_process = self.process_run_background_traffic(seq_write_parameters)
        return background_process

    def run_main_fio_benchmark(self, parameters):
        streams_mode = 1
        if parameters["non_stream"]:
            streams_mode = 2
            self.fio_process_num += 1
        if parameters["msl_average_size"]:
            self.msl = int.from_bytes(self.directives_receive(dev_name=parameters['fio']['filename']),
                                      "little") & 0xffff
            self.fio_process_num = self.msl
            log.INFO(f"Max Streams Limit: {self.msl}")
            log.INFO(f"msl_average_size is {parameters['msl_average_size']}")
            process_dict = {}
            status = 0
            output_list = []
            bw_logs_all = []
            log.INFO(f"fio process num: {self.fio_process_num}")
            nsze = int.from_bytes(self.identify_ns(dev_name=parameters['fio']['filename']),
                                  "little") & 0xffffffffffffffff
            streams_lbas = nsze // self.msl
            streams_count = self.msl
            self.set_streams(streams_lbas=streams_lbas, streams_count=streams_count, streams_mode=streams_mode,
                             block_dev=parameters['fio']['filename'])
            size = f"{parameters['size'] // self.fio_process_num}%"
            log.INFO(f"size: {size}")
            start_time = datetime.now(timezone(timedelta(hours=+8)))
            for index in range(self.fio_process_num):
                offset = f"{index * parameters['size'] // self.fio_process_num}%"
                log.INFO(f"offset: {offset}")
                out_put, bw_logs = self.set_fio_parameters(parameters["fio"])
                time.sleep(1)
                # status_dict[f"offset_{offset}"] = [0, out_put, bw_logs]
                output_list.append(out_put)
                bw_logs_all += bw_logs
                self.set_parm("offset", offset)
                self.set_parm("size", size)
                log.INFO(f"create process: offset_{offset}")
                cmd = self.parse_cmd()
                process_dict[f"offset_{offset}"] = multiprocessing.Process(target=self.call_start_fio, args=(cmd,))
            # while len(status_dict) < fio_num:
            for _, process in process_dict.items():
                process.start()
            status_list = []
            bw_moniter = multiprocessing.Process(target=self.bandwidth_monitor, args=(parameters['fio']['filename'],))
            bw_moniter.start()
            while len(process_dict) > 0:
                to_pop_key = []
                # self.bandwidth_monitor(parameters['fio']['filename'], time_to_monitor=10)
                time.sleep(5)
                for key, process in process_dict.items():
                    if not process.is_alive():
                        status = process.exitcode
                        status_list.append(status)
                        log.INFO(f"{key} status code: {status}")
                        to_pop_key.append(key)
                        log.INFO(f"process_dict len: {len(process_dict)}")
                if len(to_pop_key) > 0:
                    for key in to_pop_key:
                        process_dict.pop(key)
            if bw_moniter.is_alive():
                bw_moniter.terminate()
            self.set_streams(streams_lbas=0, streams_count=0, streams_mode=0, block_dev=parameters['fio']['filename'])
            output, result = self.analysis_results(out_puts=output_list, bw_logs=bw_logs_all, real_time=parameters["real_time"], start_time=start_time)
            return status, output, result
        else:
            parameters.get("streams_count")
            if isinstance(parameters.get("streams_count"), int) and parameters["streams_count"] > 0:
                self.set_streams(streams_count=parameters["streams_count"], streams_mode=streams_mode,
                                 block_dev=parameters['fio']['filename'])
            else:
                self.set_streams(streams_lbas=0, streams_count=0, streams_mode=0,
                                 block_dev=parameters['fio']['filename'])
            out_put, bw_logs = self.set_fio_parameters(parameters["fio"])
            start_time = datetime.now(timezone(timedelta(hours=+8)))
            log.INFO("stream fio popen")
            popen = self.popen_start_fio()
            status = self.collect_prints_util_finished(popen, parameters["real_time"])
            self.set_streams(streams_lbas=0, streams_count=0, streams_mode=0,
                             block_dev=parameters['fio']['filename'])
            output, result = self.analysis_result(out_put, bw_logs, parameters["real_time"], start_time)
            return status, output, result

    @decorate_collect_summary_result
    def analysis_json_results(self, json_string_list: list):
        # results = list()
        read_result = {"read": {}}
        write_result = {"write": {
                                  # "io": None, "bw": None, "iops": None,
                                  # "avg_latency": None, "percentiles": None,
                                  # "max_latency": None,
                                  # "min_latency": None
                                 }}
        for json_string in json_string_list:
            ret = re.findall(".*(\{[\w\W]*\}).*", json_string)
            log.INFO(f"ret: {ret}")
            if ret:
                output = json.loads(ret[0])
                jobs = output["jobs"]
                log.INFO(f"jobs: {jobs}")
                if jobs:
                    job = jobs[0]
                    job_read = self.optimization_result(job["read"])
                    job_write = self.optimization_result(job["write"])
                    for read_result_key in job_read.keys():
                        if read_result["read"].get(read_result_key) is None:
                            read_result["read"][read_result_key] = job_read[read_result_key]
                        elif read_result_key == "percentiles":
                            read_result["read"][read_result_key] = list(np.add(read_result["read"][read_result_key],
                                                                        job_read[read_result_key]))
                        else:
                            read_result["read"][read_result_key] += job_read[read_result_key]

                    for write_result_key in job_write.keys():
                        if write_result["write"].get(write_result_key) is None:
                            write_result["write"][write_result_key] = job_write[write_result_key]
                        elif write_result_key == "percentiles":
                            write_result["write"][write_result_key] = list(np.add(write_result["write"][write_result_key],
                                                                           job_write[write_result_key]))
                        else:
                            write_result["write"][write_result_key] += job_write[write_result_key]
        for read_result_key in read_result["read"].keys():
            if read_result_key.endswith("latency"):
                read_result["read"][read_result_key] /= self.fio_process_num
                log.INFO(f"read latency {read_result_key}: {read_result['read'][read_result_key]}")
            if read_result_key == "percentiles":
                read_result["read"][read_result_key] = list(np.true_divide(read_result["read"][read_result_key], self.fio_process_num))
        for write_result_key in write_result["write"].keys():
            if write_result_key.endswith("latency"):
                write_result["write"][write_result_key] /= self.fio_process_num
                log.INFO(f"write latency {write_result_key}: {write_result['write'][write_result_key]}")
            if write_result_key == "percentiles":
                write_result["write"][write_result_key] = list(np.true_divide(write_result["write"][write_result_key], self.fio_process_num))
        log.INFO(f"{read_result}\n{write_result}")
        return [read_result, write_result]

    def analysis_fio_reports(self, out_put_list: list):
        result = list()
        output = []
        for out_put in out_put_list:
            if os.path.exists(out_put):
                output.append(open(out_put).read())
            else:
                output = "Log file: {} not exist".format(out_put)
                return output, result
        log.INFO(output)
        try:
            result = self.analysis_json_results(output)
        except Exception as all_exception:
            output = f"Fio analysis_json_result failed: {out_put_list}"
            log.ERR(all_exception)
            log.ERR(output)
        return output, result

    def analysis_results(self, out_puts: list, bw_logs, real_time, start_time):
        log.INFO("analysis_results")
        log.INFO(out_puts)
        output, result = self.analysis_fio_reports(out_puts)
        log.INFO("analysis_results get result")
        if real_time != "enable":
            self.analysis_bw_logs(bw_logs, start_time)
        return output, result

    def optimization_result(self, input_dict):
        if "clat_ns" in input_dict.keys():
            clat_key = "clat_ns"
            clat_base_unit = 1000
        elif "clat_ms" in input_dict.keys():
            clat_key = "clat_ms"
            clat_base_unit = 0.001
        else:
            clat_key = "clat"
            clat_base_unit = 1
        percentile = input_dict[clat_key]["percentile"]
        percentile_list = [percentile["99.000000"]/clat_base_unit,
                           percentile["99.900000"]/clat_base_unit, percentile["99.990000"]/clat_base_unit,
                           percentile["99.999000"]/clat_base_unit, percentile["99.999900"]/clat_base_unit,
                           percentile["99.999990"]/clat_base_unit, percentile["99.999999"]/clat_base_unit]
        result = {"io": input_dict["io_bytes"], "bw": input_dict["bw"], "iops": input_dict["iops"],
                  "avg_latency": input_dict[clat_key]["mean"]/clat_base_unit, "percentiles": percentile_list,
                  "max_latency": input_dict[clat_key]["max"] / clat_base_unit,
                  "min_latency": input_dict[clat_key]["min"] / clat_base_unit}
        return result
