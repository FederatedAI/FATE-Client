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


class Task(BaseFlowAPI):
    def query(self, job_id: str = None, role: str = None, party_id: str = None, task_name: str = None,
              status: str = None, task_id: str = None, task_version: int = None):
        """
        task query info

        Args:
            job_id: job id.
            role: role, such as: "guest", "host".
            party_id: party id, such as: "9999", "10000".
            task_name: task name.
            status: task status.
            task_id: task id.
            task_version: task version.

        Returns:
        {'code': 0, 'message': 'success','data':[{...},{...}]}
        :return:
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/job/task/query', params=params)

    def query_task_list(self, limit: int = None, page: int = None, job_id: str = None, role: str = None,
                        party_id: str = None, task_name: str = None, order_by: str = None, order: str = None):
        """
        task query info

        Args:
            limit: job count of per page， use with the parameter "page", default 0
            page: job page num， use with the parameter "limit", default 0
            job_id: fuzzy matching by job id
            role:  role info, such as: "guest", "host", "arbiter"
            party_id: party id, such as: "9999", "10000"
            task_name: task name
            order_by: sort by job field, default "create_time"
            order: default "desc"

        Returns:
        {'code': 0, 'message': 'success', 'data': {"count":100,"data":[{...}, {...}]}}

        :return:
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/job/task/list/query', params=params)
