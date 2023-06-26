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


class Provider(BaseFlowAPI):
    def register(self, name: str = None, device: str = None, version: str = None, metadata: dict = None):
        """

        Args:
            name:
            device:
            version:
            metadata:

        Returns:
        {'code': 0, 'message': 'device success','data':None}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/provider/register', json=params)

    def query(self, name: str = None, device: str = None, version: str = None, provider_name: str = None):
        """

        Args:
            name:
            device:
            version:
            provider_name:

        Returns:
        {'code': 0, 'message': 'success','data':[{...},{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/provider/query', params=params)

    def delete(self, name: str = None, device: str = None, version: str = None, provider_name: str = None):
        """

        Args:
            name:
            device:
            version:
            provider_name:

        Returns:
        {'code': 0, 'message': 'success','data':{...}}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/provider/delete', json=params)


