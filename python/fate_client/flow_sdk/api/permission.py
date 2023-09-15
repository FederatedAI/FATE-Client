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


class Permission(BaseFlowAPI):
    def grant(self, app_id: str = None, role: str = None):
        """
        add role to user

        Args:
            app_id:
            role:

        Returns:
        {'code': 0, 'message': 'success','data':None}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/permission/grant', json=params)

    def delete(self, app_id: str = None, role: str = None):
        """
        delete role to user

        Args:
            app_id:
            role:

        Returns:
        {'code': 0, 'message': 'success','data':None}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/permission/delete', json=params)

    def query(self, app_id: str = None):
        """
        query user permission

        Args:
            app_id:

        Returns:
        {'code': 0, 'message': 'success','data':{...}}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/permission/query', params=params)

    def query_role(self):
        """
        query role
        Returns:
        {'code': 0, 'message': 'success','data':[...]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/permission/role/query', params=params)

    def grant_resource(self, party_id: str, component: str = None, dataset: dict = None):
        """
        grant resource
        Returns:
        {'code': 0, 'message': 'success','data':[...]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/permission/resource/grant', json=params)

    def delete_resource(self, party_id: str, component: str = None, dataset: dict = None):
        """
        delete resource
        Returns:
        {'code': 0, 'message': 'success','data':[...]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._post(url='/permission/resource/delete', json=params)

    def query_resource(self, party_id: str, component: str = None, dataset: dict = None):
        """
        delete resource
        Returns:
        {'code': 0, 'message': 'success','data':[...]}
        """
        kwargs = locals()
        params = filter_invalid_params(**kwargs)
        return self._get(url='/permission/resource/query', params=params)



