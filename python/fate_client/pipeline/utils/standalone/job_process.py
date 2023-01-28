#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import copy
import multiprocessing
import psutil
import subprocess
import time

from pathlib import Path
from types import SimpleNamespace
from ...scheduler.runtime_constructor import RuntimeConstructor


WAIT_BEFORE_TERMINATE = 5
WAIT_BEFORE_KILL = 5


def run_subprocess(exec_cmd, std_log_fd):
    process = subprocess.Popen(
        exec_cmd,
        stderr=std_log_fd,
        stdout=std_log_fd
    )
    return process


def run_task_in_party(exec_cmd, std_log_fd, pid_record_path, status_manager, party_task_id):
    process = run_subprocess(exec_cmd, std_log_fd)

    with open(pid_record_path, "w") as fout:
        fout.write(str(process.pid) + "\n")
        fout.flush()

    process.communicate()
    process.terminate()
    if process.returncode != 0:
        """
        subprocess fail, record the fail status to MLMD
        """
        status_manager.record_task_status(party_task_id, "exception")


def run_detect_task(status_manager, party_task_ids, pid_record_paths):
    while True:
        is_finish = status_manager.monitor_finish_status(party_task_ids)
        if is_finish:
            status_manager.record_terminate_status(party_task_ids)
            time.sleep(0.5)
            for pid_record_path in pid_record_paths:
                with open(pid_record_path, "r") as fin:
                    pid = int(fin.read())
                    try:
                        p = psutil.Process(int(pid))
                    except psutil.NoSuchProcess:
                        continue

                    for i in range(WAIT_BEFORE_TERMINATE):
                        if p.is_running():
                            time.sleep(1)
                        else:
                            pass

                    try:
                        if p.is_running():
                            p.terminate()
                    except BaseException:
                        continue
                    finally:
                        for i in range(WAIT_BEFORE_KILL):
                            if p.is_running():
                                time.sleep(1)
                            else:
                                break
                        try:
                            if p.is_running():
                                p.kill()
                        except BaseException:
                            pass

            break

        time.sleep(0.5)


def process_task(task_type: str, task_name: str, exec_cmd_prefix: list, runtime_constructor: RuntimeConstructor):
    parties = runtime_constructor.runtime_parties
    task_pools = list()
    status_manager = runtime_constructor.status_manager
    # task_done_tag_paths = list()
    mp_ctx = multiprocessing.get_context("fork")
    std_log_fds = []
    pid_record_paths = []
    party_task_ids = []
    task_infos = []
    for party in parties:
        role = party.role
        party_id = party.party_id

        conf_path = runtime_constructor.task_conf_path(role, party_id)
        party_task_id = runtime_constructor.party_task_id(role, party_id)
        party_task_ids.append(party_task_id)
        task_infos.append(SimpleNamespace(party_task_id=party_task_id, role=role, party_id=party_id))

        log_path = runtime_constructor.log_path(role, party_id)
        std_log_path = Path(log_path).joinpath("std.log").resolve()
        std_log_path.parent.mkdir(parents=True, exist_ok=True)
        std_log_fd = open(std_log_path, "w")
        std_log_fds.append(std_log_fd)
        pid_record_path = Path(log_path).joinpath("pid.log").resolve()
        pid_record_paths.append(pid_record_path)

        exec_cmd = copy.deepcopy(exec_cmd_prefix)
        exec_cmd.extend(
            [
                "--process-tag",
                party_task_id,
                "--config",
                conf_path
            ]
        )
        task_pools.append(mp_ctx.Process(target=run_task_in_party, kwargs=dict(
            exec_cmd=exec_cmd,
            std_log_fd=std_log_fd,
            pid_record_path=pid_record_path,
            status_manager=status_manager,
            party_task_id=party_task_id
        )))

        task_pools[-1].start()

    detect_task = mp_ctx.Process(target=run_detect_task,
                                 kwargs=dict(status_manager=status_manager,
                                             party_task_ids=party_task_ids,
                                             pid_record_paths=pid_record_paths))

    detect_task.start()

    detect_task.join()
    for func in task_pools:
        func.join()

    for std_log_fd in std_log_fds:
        std_log_fd.close()

    return status_manager.get_task_results(task_infos)
