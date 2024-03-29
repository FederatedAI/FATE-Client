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
from ..utils.base_utils import BaseFlowAPI
from ..utils.params_utils import filter_invalid_params


class Log(BaseFlowAPI):
    def count(self, log_type: str = None, job_id: bool = None, role: str = None, party_id: str = None,
              task_name: int = None, instance_id: str = None):
        """
        get log file count

        Args:
            log_type: log type such as: "task_error","task_warning","task_error","task_debug","fate_flow_schedule","fate_flow_schedule_error".
            job_id: job id.
            role: role, such as: "guest", "host".
            party_id: party id, such as: "9999", "10000".
            task_name: task name, such as:'psi_0...'
            instance_id: instance id.

        Returns:
        {'code': 0, 'message': 'success','data':num]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/log/count', params=params)

    def query(self, log_type: str = None, job_id: bool = None, role: str = None, party_id: str = None,
              task_name: int = None, begin: int = None, end: int = None, instance_id: str = None):
        """
        query log

        Args:
            log_type: log type such as: "info","warning","error","debug","fate_flow_schedule","fate_flow_schedule_error".
            job_id: job id.
            role: role, such as: "guest", "host".
            party_id: party id, such as: "9999", "10000".
            task_name: task name, such as:'psi_0',...
            begin: num, starting line number.
            end: num, ending line number.
            instance_id: instance id.
        Returns:
            {'code': 0, 'message': 'success','data':[]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/log/query', params=params)
