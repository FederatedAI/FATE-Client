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
from typing import Dict, Union
from ..utils.base_utils import BaseFlowAPI
from ..utils.io_utils import download_from_request
from ..utils.params_utils import filter_invalid_params


class Client(BaseFlowAPI):
    def create_client(self, app_name: str = None):
        """
        Create client

        Args:
            app_name: app name

        Returns:
            {"code":0,"data":{"app_name":"xxx","app_id":"xxx","app_token":"xxx","app_type":"xxx"},"message":"success"}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/app/client/create', json=params)

    def delete_client(self, app_id: str = None):
        """
        Delete client

        Args:
            app_id: app_id.

        Returns:
        {"code":0,"data":{"status":"xxx"},"message":"success"}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/app/client/delete', json=params)

    def query_client(self, app_id: str = None, app_name: str = None):
        """
        Query client

        Args:
            app_id: app_id.
            app_name: app_name.

        Returns:
        {"code":0,"data":{"xxx":"xxx",},"message":"success"}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/app/client/query', params=params)

    def create_site(self, party_id: str = None):
        """
        Create site

        Args:
            party_id: party_id

        Returns:
            {"code":0,"data":{"app_id":"xxx","app_token":"xxx","party_id":"xxx"},"message":"success"}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/app/site/create', json=params)

    def delete_site(self, party_id: str = None):
        """
        Delete site

        Args:
            party_id: party_id.

        Returns:
        {"code":0,"data":{"status":"xxx"},"message":"success"}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/app/site/delete', json=params)

    def query_site(self, party_id: str = None):
        """
        Query client

        Args:
            party_id: party_id.

        Returns:
        {"code":0,"data":{"xxx":"xxx",},"message":"success"}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/app/site/query', params=params)

    def create_partner(self, app_id: str = None, party_id: str = None, app_token: str = None):
        """
        Create partner

        Args:
            app_id: app_id
            party_id: party_id
            app_token: app_token

        Returns:
            {"code":0,"data":{"app_id":"xxx","app_token":"xxx","party_id":"xxx"},"message":"success"}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/app/partner/create', json=params)

    def delete_partner(self, party_id: str = None):
        """
        Delete client

        Args:
            party_id: party_id.

        Returns:
        {"code":0,"data":{"status":"xxx"},"message":"success"}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/app/partner/delete', json=params)

    def query_partner(self, party_id: str = None):
        """
        Query client

        Args:
            party_id: party_id.

        Returns:
        {"code":0,"data":{"xxx":"xxx",},"message":"success"}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/app/partner/query', params=params)
