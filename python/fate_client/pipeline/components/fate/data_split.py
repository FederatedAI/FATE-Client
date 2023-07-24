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

from ..component_base import Component
from ...conf.types import PlaceHolder
from ...interface import ArtifactType


class DataSplit(Component):
    yaml_define_path = "./component_define/fate/data_split.yaml"

    def __init__(self,
                 _name: str,
                 runtime_roles: List[str] = None,
                 input_data: ArtifactType = PlaceHolder(),
                 train_size: int = None,
                 validate_size: int = None,
                 test_size: int = None,
                 stratified: bool = False,
                 random_state: int = None,
                 federated_sample: bool = True
                 ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(DataSplit, self).__init__()
        self._name = _name
        self.runtime_roles = runtime_roles
        self.input_data = input_data
        self.train_size = train_size
        self.validate_size = validate_size
        self.test_size = test_size
        self.stratified = stratified
        self.random_state = random_state
        self.federated_sample = federated_sample
