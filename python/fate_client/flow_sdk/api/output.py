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
    def query_metric_key(self, job_id: str, role: str, party_id: str, task_name: str):
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

    def query_metric(self, job_id: str, role: str, party_id: str, task_name: str, filters: dict = None):
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

    def delete_metric(self, job_id: str, role: str, party_id: str, task_name: str):
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

    def query_model(self, job_id: str, role: str, party_id: str, task_name: str):
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

    def delete_model(self, job_id: str, role: str, party_id: str, task_name: str):
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

    def download_data(self, job_id: str, role: str, party_id: str, task_name: str, output_key: str = None):
        """

        Args:
            job_id:
            role:
            party_id:
            task_name:
            output_key:


        Returns:
        {'code': 0, 'message': 'success','data':dict}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/output/data/download', json=params)