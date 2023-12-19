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
from typing import List

from fate_client.pipeline.components.component_base import Component
from fate_client.pipeline.conf.types import PlaceHolder
from fate_client.pipeline.interface import ArtifactType


class Intersection(Component):
    yaml_define_path = "./adapters/bfia/component_define/unionpay/intersection.yaml"

    def __init__(
        self,
        _name: str,
        runtime_parties: dict = None,
        id: str = PlaceHolder(),
        intersect_method: str = PlaceHolder(),
        sync_intersect_ids: bool = PlaceHolder(),
        only_output_key: bool = PlaceHolder(),
        use_hash: bool = PlaceHolder(),
        hash_method: str = PlaceHolder(),
        final_hash_method: str = PlaceHolder(),
        raw_params: str = PlaceHolder(),
        rsa_params: str = PlaceHolder(),
        key_length: int = PlaceHolder(),
        salt: str = PlaceHolder(),
        base64: bool = PlaceHolder(),
        join_role: str = PlaceHolder(),
        train_data: ArtifactType = PlaceHolder()
    ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(Intersection, self).__init__()
        self._name = _name
        self.runtime_parties = runtime_parties
        self.id = id
        self.intersect_method = intersect_method
        self.syn_intersect_ids = sync_intersect_ids
        self.only_output_key = only_output_key
        self.use_hash = use_hash
        self.hash_method = hash_method
        self.final_hash_method = final_hash_method
        self.raw_params = raw_params
        self.rsa_param = rsa_params
        self.key_length = key_length
        self.salt = salt
        self.base64 = base64
        self.join_role = join_role
        self.train_data = train_data

