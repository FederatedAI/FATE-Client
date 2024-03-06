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
import json
from ..utils.base_utils import BaseFlowAPI
from ..utils.params_utils import filter_invalid_params
from ..utils.io_utils import download_from_request


class Data(BaseFlowAPI):
    def upload(self, file: str, head: bool, partitions: int, meta: dict, namespace: str = None, name: str = None,
               extend_sid: bool = None, role: str = None, party_id: str = None):
        """
        upload data

        Args:
            file: file, such as: "/data/xxx.csv"
            head: bool
            namespace: namespace
            name: name
            partitions: num
            extend_sid: bool
            meta: meta
            role: role, such as: "guest", "host".
            party_id: party id.

        Returns:
            {'code': 0, 'message': 'success','data':{...}]}
        """
        kwargs = locals()
        # if not os.path.exists(file):
        #     raise Exception(f"{file} is not exist, please check the file path")
        params = filter_invalid_params(**kwargs)
        return self._post(url='/data/component/upload', json=params)

    def upload_file(self, file: str, head: bool, partitions: int, meta: dict, namespace: str = None, name: str = None,
                    extend_sid: bool = None, role: str = None, party_id: str = None):
        """
       upload file

        Args:
            file: file, such as: "/data/xxx.csv"
            head: bool
            namespace: namespace
            name: name
            partitions: num
            extend_sid: bool
            meta: meta
            role: role, such as: "guest", "host".
            party_id: party id.

        Returns:
            {'code': 0, 'message': 'success','data':{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        file_path = params.pop("file")
        files = {'file': open(file_path, 'rb')}
        meta = params.pop("meta")
        params["meta"] = json.dumps(meta)

        return self._post(url='/data/component/upload/file', files=files, data=params, handle_result=True)

    def dataframe_transformer(self, namespace: str, name: str, data_warehouse: dict, drop: bool = True,
                              site_name: str = None):
        """
        Args:
            namespace: namespace
            name: name
            data_warehouse: {"namespace": xxx, "name": xxx}
            drop: destroy table if the table exist
            site_name: site name

        Returns:
            {'code': 0, 'message': 'success','data':{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/data/component/dataframe/transformer', json=params)

    def download(self, namespace: str = None, name: str = None, path: str = None):
        """
        download data

        Args:
            namespace: namespace
            name: name

        Returns:
            {'code': 0, 'message': 'success','data':{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        resp = self._get(url='/data/download', params=params, handle_result=False)
        return download_from_request(resp, path)

    def download_component(self, namespace: str = None, name: str = None, path: str = None):
        """
        download component

        Args:
            namespace:
            name:

        Returns:
            {'code': 0, 'message': 'success','data':{...}]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/data/component/download', json=params)
