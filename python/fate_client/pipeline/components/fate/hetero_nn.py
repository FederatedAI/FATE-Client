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
from ...conf.types import PlaceHolder
from ..component_base import Component
from ...interface import ArtifactType


class HeteroNN(Component):
    yaml_define_path = "./component_define/fate/hetero_nn.yaml"

    def __init__(
        self,
        _name: str,
        runtime_roles: List[str] = None,
        runner_module: str = PlaceHolder(),
        runner_class: str = PlaceHolder(),
        runner_conf: dict = PlaceHolder(),
        source: str = PlaceHolder(),
        train_data: ArtifactType = PlaceHolder(),
        validate_data: ArtifactType = PlaceHolder(),
        test_data: ArtifactType = PlaceHolder(),
        train_model_input: ArtifactType = PlaceHolder(),
        predict_model_input: ArtifactType = PlaceHolder(),
    ):

        inputs = locals()
        self._process_init_inputs(inputs)
        super(HeteroNN, self).__init__()
        self._name = _name
        self.runtime_roles = runtime_roles
        self.runner_module = runner_module
        self.runner_class = runner_class
        self.runner_conf = runner_conf
        self.source = source
        self.train_data = train_data
        self.validate_data = validate_data
        self.test_data = test_data
        self.train_model_input = train_model_input
        self.predict_model_input = predict_model_input