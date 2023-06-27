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


class Data(BaseFlowAPI):
    def upload(self, file: str = None, head: bool = None, namespace: str = None, name: str = None,
              partitions: int = None, storage_engine: str = None, destroy: bool = None, meta: dict = None):
        """
        upload file

        Args:
            file: file
            head:
            namespace:
            name:
            partitions:
            storage_engine:
            destroy:
            meta:

        Returns:
        {'code': 0, 'message': 'success','data':{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/data/upload', json=params)

    def dataframe_transformer(self, namespace: str = None, name: str = None, data_warehouse: dict = None):
        """
        upload file

        Args:
            namespace:
            name:
            data_warehouse:

        Returns:
        {'code': 0, 'message': 'success','data':{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/data/dataframe/transformer', json=params)

    def download(self, namespace: str = None, name: str = None):
        """
        download

        Args:
            namespace:
            name:

        Returns:

        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/data/download', params=params)
