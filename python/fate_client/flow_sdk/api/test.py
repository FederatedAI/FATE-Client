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
import os.path
from ..utils.base_utils import BaseFlowAPI
from ..utils.params_utils import filter_invalid_params


class Test(BaseFlowAPI):
    def toy(self, guest_party_id: str, host_party_id: str, guest_user_name: str = "", host_user_name: str = "",
            task_cores: int = 2, timeout: int = 60):
        kwargs = locals()
        dag_schema = self.toy_conf(**kwargs)
        return self._post(url='/job/submit', json={'dag_schema': dag_schema})

    @classmethod
    def toy_conf(cls, guest_party_id: str, host_party_id: str, task_cores: int = 2, **kwargs):
        job_conf = {
            'dag':
                {
                    'parties': [
                        {'party_id': [guest_party_id], 'role': 'guest'},
                        {'party_id': [host_party_id], 'role': 'host'}],
                    'stage': 'default',
                    'tasks': {
                        'toy_example_0': {
                            'component_ref': 'toy_example',
                            'parameters': {'data_num': 1024, 'partition': 4}
                        }
                    }
                },
            'schema_version': '2.0.0.alpha'
        }

        return job_conf

    @classmethod
    def toy_dsl(cls):
        dsl = {
            "components": {
                "secure_add_example_0": {
                    "module": "SecureAddExample"
                }
            }
        }
        return dsl

    @classmethod
    def check_toy(cls, guest_party_id, job_status, log_dir):
        if job_status in {"canceled"}:
            info_log = os.path.join(log_dir, "guest", guest_party_id, "toy_example_0", "root", "INFO")
            with open(info_log, "r") as fin:
                for line in fin:
                    if line.find("secure_add_guest") != -1:
                        yield line.strip()
        else:
            error_log = os.path.join(log_dir, "guest", guest_party_id, "ERROR")
            with open(error_log, "r") as fin:
                for line in fin:
                    yield line.strip()
