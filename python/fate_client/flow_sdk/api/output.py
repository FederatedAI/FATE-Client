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


class Output(BaseFlowAPI):
    def metric_key_query(self, job_id: str = None, role: str = None, party_id: str = None, task_name: str = None):
        """

        Args:
            job_id:
            role:
            party_id:
            task_name:


        Returns:
        {'code': 0, 'message': 'success','data':[{...},{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/output/metric/key/query', params=params)

    def metric_query(self, job_id: str = None, role: str = None, party_id: str = None, task_name: str = None,
                     filters: dict = None):
        """

        Args:
            job_id:
            role:
            party_id:
            task_name:
            filters:


        Returns:
        {'code': 0, 'message': 'success','data':[{...},{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/output/metric/query', params=params)

    def metric_delete(self, job_id: str = None, role: str = None, party_id: str = None, task_name: str = None):
        """

        Args:
            job_id:
            role:
            party_id:
            task_name:


        Returns:
        {'code': 0, 'message': 'success','data':bool}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/output/metric/delete', json=params)

    def model_query(self, job_id: str = None, role: str = None, party_id: str = None, task_name: str = None):
        """

        Args:
            job_id:
            role:
            party_id:
            task_name:


        Returns:
        {'code': 0, 'message': 'success','data':str}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/output/model/query', params=params)

    def model_delete(self, job_id: str = None, role: str = None, party_id: str = None, task_name: str = None):
        """

        Args:
            job_id:
            role:
            party_id:
            task_name:


        Returns:
        {'code': 0, 'message': 'success','data':dict}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/output/model/delete', json=params)

