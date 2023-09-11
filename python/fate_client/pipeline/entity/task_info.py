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
import abc
from .model_info import FateFlowModelInfo
from ..utils.fateflow.fate_flow_job_invoker import FATEFlowJobInvoker


class TaskInfo(object):
    def __init__(self, task_name: str, model_info: FateFlowModelInfo):
        self._model_info = model_info
        self._task_name = task_name

    @abc.abstractmethod
    def get_output_data(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    def get_output_model(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    def get_output_metric(self, *args, **kwargs):
        ...


class FateFlowTaskInfo(TaskInfo):
    def get_output_model(self):
        return FATEFlowJobInvoker().get_output_model(job_id=self._model_info.job_id,
                                                     role=self._model_info.local_role,
                                                     party_id=self._model_info.local_party_id,
                                                     task_name=self._task_name)

    def get_output_data(self):
        return FATEFlowJobInvoker().get_output_data(job_id=self._model_info.job_id,
                                                    role=self._model_info.local_role,
                                                    party_id=self._model_info.local_party_id,
                                                    task_name=self._task_name)

    def get_output_metric(self):
        return FATEFlowJobInvoker().get_output_metric(job_id=self._model_info.job_id,
                                                      role=self._model_info.local_role,
                                                      party_id=self._model_info.local_party_id,
                                                      task_name=self._task_name)



