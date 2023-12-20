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
#
import os
import tempfile
import time
from datetime import timedelta
from pathlib import Path

from fate_client.flow_sdk import FlowClient
from ...conf.env_config import FlowConfig


class FATEFlowJobInvoker(object):
    def __init__(self):
        self._client = FlowClient(ip=FlowConfig.IP, port=FlowConfig.PORT, version=FlowConfig.VERSION)

    def monitor_status(self, job_id, role, party_id):
        start_time = time.time()
        pre_task = None
        print(f"Job id is {job_id}\n")
        while True:
            response_data = self.query_job(job_id, role, party_id)
            status = response_data["status"]
            if status == JobStatus.SUCCESS:
                elapse_seconds = timedelta(seconds=int(time.time() - start_time))
                print(f"Job is success!!! Job id is {job_id}, response_data={response_data}")
                print(f"Total time: {elapse_seconds}")
                break

            elif status == JobStatus.RUNNING:
                code, data = self.query_task(job_id=job_id, role=role, party_id=party_id,
                                             status=JobStatus.RUNNING)

                if code != 0 or len(data) == 0:
                    time.sleep(0.1)
                    continue

                elapse_seconds = timedelta(seconds=int(time.time() - start_time))
                if len(data) == 1:
                    task = data[0]["task_name"]
                else:
                    task = []
                    for task_data in data:
                        task.append(task_data["task_name"])

                if task != pre_task:
                    print(f"\r")
                    pre_task = task
                print(f"\x1b[80D\x1b[1A\x1b[KRunning task {task}, time elapse: {elapse_seconds}")

            elif status == JobStatus.WAITING:
                elapse_seconds = timedelta(seconds=int(time.time() - start_time))
                print(f"\x1b[80D\x1b[1A\x1b[KJob is waiting, time elapse: {elapse_seconds}")

            elif status in [JobStatus.FAILED, JobStatus.CANCELED]:
                raise ValueError(f"Job is {status}, please check out job_id={job_id} in fate_flow log directory")

            time.sleep(1)

    def submit_job(self, dag_schema):
        response = self._client.job.submit(dag_schema=dag_schema)
        try:
            code = response["code"]
            if code != 0:
                raise ValueError(f"Return code {code}!=0")

            job_id = response["job_id"]
            model_id = response["data"]["model_id"]
            model_version = response["data"]["model_version"]
            return job_id, model_id, model_version
        except BaseException:
            raise ValueError(f"submit job is failed, response={response}")

    def query_job(self, job_id, role, party_id):
        response = self._client.job.query(job_id, role, party_id)
        try:
            code = response["code"]
            if code != 0:
                raise ValueError(f"Return code {code}!=0")

            data = response["data"][0]
            return data
        except BaseException:
            raise ValueError(f"query job is failed, response={response}")

    def query_task(self, job_id, role, party_id, status):
        response = self._client.task.query(job_id=job_id, role=role, party_id=party_id, status=status)
        try:
            code = response["code"]
            data = response.get("data", [])
            return code, data
        except BaseException:
            raise ValueError(f"query task is failed, response={response}")

    def query_site_info(self):
        response = self._client.site.info()
        try:
            code = response["code"]
            if code != 0:
                return None

            party_id = response["data"]["party_id"]
            return party_id
        except ValueError:
            return None

    def bind_local_path(self, path, namespace, name):
        response = self._client.table.bind_path(path=path, namespace=namespace, name=name)
        try:
            code = response["code"]
            if code != 0:
                raise ValueError(f"Return code {code} != 0")
            print(f"bind path success")
        except BaseException:
            raise ValueError(f"bind path fails, response={response}")

    def upload_file_and_convert_to_dataframe(
            self, file, meta, head, extend_sid,
            namespace, name, role=None, party_id=None, **kwargs):
        response = self._client.data.upload_file(file=file,
                                                 head=head,
                                                 meta=meta,
                                                 extend_sid=extend_sid,
                                                 namespace=namespace,
                                                 name=name,
                                                 **kwargs)
        try:
            code = response["code"]
            if code != 0:
                raise ValueError(f"Return code {code}!=0")

            job_id = response["job_id"]
        except BaseException:
            raise ValueError(f"Upload data fails, response={response}")

        self.monitor_status(job_id, role=role, party_id=party_id)

    def get_output_data(self, job_id, role, party_id, task_name):
        with tempfile.TemporaryDirectory() as data_dir:
            response = self._client.output.download_data(job_id=job_id, role=role, party_id=party_id,
                                                         task_name=task_name, path=data_dir)
            try:
                code = response["code"]
                if code != 0:
                    raise ValueError(f"Return code {code}!=0")
            except BaseException:
                raise ValueError(f"query task={job_id}, role={role}, "
                                 f"party_id={party_id}'s output data is failed, response={response}")

            data_dir = Path(data_dir).joinpath(os.listdir(data_dir)[0])
            output_keys = os.listdir(data_dir)
            if not output_keys:
                return None

            output_data_dict = {}
            for output_key in output_keys:
                path = Path(data_dir).joinpath(output_key)
                files = os.listdir(path)
                file_names = []
                for file in files:
                    if file.endswith("csv"):
                        file_names.append(file)

                if len(file_names) == 1:
                    output_data_dict[output_key] = self.load_data_to_pd_df(path.joinpath(file_names[0]))
                else:
                    output_data_dict[output_key] = dict()
                    for file_name in file_names:
                        output_data_dict[output_key][file_name] = self.load_data_to_pd_df(path.joinpath(file_name))

            return output_data_dict

    def get_output_model(self, job_id, role, party_id, task_name):
        response = self._client.output.query_model(job_id=job_id, role=role, party_id=party_id, task_name=task_name)
        try:
            code = response["code"]
            if code != 0:
                raise ValueError(f"Return code {code}!=0")
            model = response["data"]
            return model
        except BaseException:
            raise ValueError(f"query task={job_id}, role={role}, "
                             f"party_id={party_id}'s output model is failed, response={response}")

    def get_output_metric(self, job_id, role, party_id, task_name):
        response = self._client.output.query_metric(job_id=job_id, role=role, party_id=party_id, task_name=task_name)
        try:
            code = response["code"]
            if code != 0:
                raise ValueError(f"Return code {code}!=0")
            metrics = response["data"]
            return metrics
        except BaseException:
            raise ValueError(f"query task={job_id}, role={role}, "
                             f"party_id={party_id}'s output metrics is failed, response={response}")

    @staticmethod
    def load_data_to_pd_df(path: Path):
        import pandas as pd
        import json
        is_predict_task = False
        template_col_names = ["label", "predict_result", "predict_score", "predict_detail", "type"]

        with open(path, "r") as fin:
            columns = set(fin.readline().strip().split(",", -1))
            tot = 0
            for col in template_col_names:
                if col in columns:
                    tot += 1

            if tot >= 4:
                is_predict_task = True

        if is_predict_task:
            data = []
            columns = None
            with open(path, "r") as fin:
                for line in fin:
                    if not columns:
                        columns = line.strip().split(",")
                    else:
                        cols = line.strip().split(",", -1)
                        predict_detail = json.loads(",".join(cols[len(columns) - 2: -1])[1:-1].replace("\'", "\""))
                        value = cols[: len(columns) - 2] + [predict_detail] + cols[-1:]
                        data.append(value)
            return pd.DataFrame(data, columns=columns)
        else:
            return pd.read_csv(path)


class JobStatus(object):
    WAITING = 'waiting'
    READY = 'ready'
    RUNNING = "running"
    CANCELED = "canceled"
    TIMEOUT = "timeout"
    FAILED = "failed"
    PASS = "pass"
    SUCCESS = "success"
