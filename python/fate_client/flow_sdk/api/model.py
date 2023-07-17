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


class Model(BaseFlowAPI):
    def deploy(self, model_id: str = None, model_version: int = None):
        """

        Args:
            model_id:
            model_version:


        Returns:
        {'code': 0, 'message': 'success','data':{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        # todo
        return self._post(url='/model/deploy', params=params)

    def load(self):
        """

        Args:
            namespace:
            name:

        Returns:

        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/model/load', params=params)

    def migrate(self, role: str, model_id: str, model_version: str, party_id: str, dir_path: str):
        """

        Args:


        Returns:

        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/model/migrate', params=params)

    def export(self, role: str, model_id: str, model_version: str, party_id: str, path: str):
        """

        Args:

        Returns:

        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/model/local/export', json=params)

    def import_model(self):
        """

        Args:

        Returns:

        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/model/import', params=params)

    def store(self):
        """

        Args:

        Returns:

        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/model/store', params=params)

    def restore(self):
        """

        Args:

        Returns:

        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/model/restore', params=params)