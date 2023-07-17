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
from ..utils.io_utils import download_from_request


class Data(BaseFlowAPI):
    def upload(self, file: str, head: bool, partitions: int, meta: dict, namespace: str = None, name: str = None,
               extend_sid: bool = None, role: str = None, party_id: str = None):
        """
        upload file

        Args:
            file: file
            head:
            namespace:
            name:
            partitions:
            extend_sid:
            meta:
            role:
            party_id:



        Returns:
        {'code': 0, 'message': 'success','data':{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        response = self._post(url='/data/component/upload/', json=params)
        if response.json()['code'] != 0:
            return response
        else:
            print(f'upload success:{response.json()}')
            response = self.dataframe_transformer(namespace=namespace, name=name, data_warehouse={"data_warehouse": response.json()['data']})
            return response

    def dataframe_transformer(self, namespace: str, name: str, data_warehouse: dict):
        """
        upload file

        Args:
            namespace:
            name:
            data_warehouse: {"namespace": xxx, "name": xxx}
            role:
            party_id:

        Returns:
        {'code': 0, 'message': 'success','data':{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/data/component/dataframe/transformer', json=params)

    def download(self, namespace: str = None, name: str = None, path: str = None):
        """
        download

        Args:
            namespace:
            name:

        Returns:

        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        resp = self._get(url='/data/download', params=params, handle_result=False)
        if path:
            return download_from_request(resp, path)
        else:
            return resp

    def download_component(self, namespace: str = None, name: str = None, path: str = None):
        """
        download

        Args:
            namespace:
            name:

        Returns:

        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/data/component/download', json=params)
