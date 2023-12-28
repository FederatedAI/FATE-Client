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


class Model(BaseFlowAPI):
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
        export model data
        Args:
            role: role.
            model_id: model_id.
            model_version: model_version.
            party_id: party_id.
            path: path, /data/xxx
        Returns:
            {"code":0,"data":{"status":"xxx"},"message":"success"}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/model/export', json=params)

    def import_model(self, model_id: str, model_version: str, path: str):
        """
        import model data
        Args:
            model_id: model_id.
            model_version: model_version.
            path: path, /data/xxx.
        Returns:

        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        files = {'file': open(path, 'rb')}
        return self._post(url='/model/import', data=params, files=files, handle_result=False)

    def delete_model(self, model_id: str, model_version: str, role: str = None,
                     party_id: str = None, task_name: str = None, output_key: str = None):
        """
        delete model
        Args:
            model_id: model_id
            model_version: model_version
            role: role, such as: "guest", "host"
            party_id: party id, such as: "9999", "10000"
            task_name: task name
            output_key: output key, Primary key for output data or model of the task
        Returns:

        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/model/delete', json=params)

    def store(self):
        """

        Args:

        Returns:

        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/model/store', json=params)

    def restore(self):
        """

        Args:

        Returns:

        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/model/restore', json=params)