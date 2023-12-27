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

from ..utils.base_utils import BaseFlowAPI
from ..utils.params_utils import filter_invalid_params
from ..utils.io_utils import download_from_request


class Output(BaseFlowAPI):
    def query_metric_key(self, job_id: str, role: str, party_id: str, task_name: str):
        """
        query metric key
        Args:
            job_id: job id.
            role:  role, such as: "guest", "host".
            party_id: party id.
            task_name: task name.

        Returns:
        {'code': 0, 'message': 'success','data':[{...},{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/output/metric/key/query', params=params)

    def query_metric(self, job_id: str, role: str, party_id: str, task_name: str, filters: dict = None):
        """
        query metric
        Args:
            job_id: job id.
            role: role, such as: "guest", "host".
            party_id: party id.
            task_name: task name.
            filters: filters, filter conditions.


        Returns:
        {'code': 0, 'message': 'success','data':[{...},{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/output/metric/query', params=params)

    def delete_metric(self, job_id: str, role: str, party_id: str, task_name: str):
        """

        Args:
            job_id: job id
            role: role, such as: "guest", "host".
            party_id: party id.
            task_name: task name.


        Returns:
        {'code': 0, 'message': 'success','data':bool}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/output/metric/delete', json=params)

    def query_model(self, job_id: str, role: str, party_id: str, task_name: str):
        """

        Args:
            job_id: job id
            role: role, such as: "guest", "host".
            party_id: party id.
            task_name: task name.

        Returns:
        {'code': 0, 'message': 'success','data':str}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/output/model/query', params=params)

    def download_model(self, job_id: str, role: str, party_id: str, task_name: str, path: str = None):
        """
        download model
        Args:
            job_id: job id.
            role: role, such as: "guest", "host".
            party_id: party id.
            task_name: task name.
            path: path, such as: /data/projects/xxx

        Returns:
        {'code': 0, 'message': 'success','data':{}}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        resp = self._get(url='/output/model/download', params=params, handle_result=False)
        if path:
            extract_dir = os.path.join(path, f'output_model_{job_id}_{role}_{party_id}_{task_name}')
            return download_from_request(resp, extract_dir)
        else:
            return resp

    def delete_model(self, job_id: str, role: str, party_id: str, task_name: str):
        """
        delete model
        Args:
            job_id: job id.
            role: role, such as: "guest", "host".
            party_id: party id.
            task_name: task name.

        Returns:
        {'code': 0, 'message': 'success'}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/output/model/delete', json=params)

    def download_data(
            self, job_id: str, role: str, party_id: str, task_name: str, output_key: str = None, path: str = None
    ):
        """
        download data
        Args:
            job_id: job id.
            role: role, such as: "guest", "host".
            party_id:  party id.
            task_name: task name.
            output_key: output key.
            path: download path, such as: /data/projects/xxx.

        Returns:
            If "download_dir" is passed, json will be returned, eg: {'code': 0, 'message': 'download success, please check the path'}
            else return tar.gz stream
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        resp = self._get(url='/output/data/download', params=params, handle_result=False)
        if path:
            extract_dir = os.path.join(path, f'output_data_{job_id}_{role}_{party_id}_{task_name}')
            return download_from_request(resp, extract_dir)
        else:
            return resp

    def data_table(self, job_id: str, role: str, party_id: str, task_name: str):
        """

        Args:
            job_id: job id.
            role:  role, such as: "guest", "host".
            party_id: party id.
            task_name: task name.

        Returns:
            {'code': 0, 'message': 'success','data':{}}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/output/data/table', params=params)

    def data_display(self, job_id: str, role: str, party_id: str, task_name: str):
        """

        Args:
            job_id: job id.
            role: role, such as: "guest", "host".
            party_id: party id.
            task_name: task name.

        Returns:
            {'code': 0, 'message': 'success','data': [...]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/output/data/display', params=params)
