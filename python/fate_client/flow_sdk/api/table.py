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


class Table(BaseFlowAPI):
    def query(self, namespace: str = None, name: str = None, display: bool = False):
        """
        query table
        Args:
            namespace: namespace
            name: name
            display: bool

        Returns:
        {'code': 0, 'message': 'success','data':{...}}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/table/query', params=params)

    def delete(self, namespace: str = None, name: str = None):
        """
        delete table
        Args:
            namespace: namespace
            name: name

        Returns:
        {'code': 0, 'message': 'success','data':{...}}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/table/delete', json=params)

    def bind_path(self, namespace: str, name: str, path: str):
        """
        bind path
        Args:
            namespace: namespace
            name: name
            path: path, /data/xxx

        Returns:
        {'code': 0, 'message': 'success'}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/table/bind/path', json=params)



