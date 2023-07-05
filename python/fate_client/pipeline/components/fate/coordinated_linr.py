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


class CoordinatedLinR(Component):
    yaml_define_path = "./component_define/fate/coordinated_linr.yaml"

    def __init__(self,
                 _name: str,
                 runtime_roles: List[str] = None,
                 max_iter: int = 20,
                 early_stop: str = "diff",
                 tol: float = 1e-4,
                 batch_size: int = -1,
                 optimizer: dict = PlaceHolder(),
                 learning_rate_scheduler: dict = PlaceHolder(),
                 init_param: dict = PlaceHolder(),
                 train_data: ArtifactType = PlaceHolder(),
                 validate_data: ArtifactType = PlaceHolder(),
                 test_data: ArtifactType = PlaceHolder(),
                 input_model: ArtifactType = PlaceHolder()
                 ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(CoordinatedLinR, self).__init__()
        self._name = _name
        self.runtime_roles = runtime_roles
        self.max_iter = max_iter
        self.early_stop = early_stop
        self.tol = tol
        self.batch_size = batch_size
        self.optimizer = optimizer
        self.learning_rate_scheduler = learning_rate_scheduler
        self.init_param = init_param
        self.train_data = train_data
        self.validate_data = validate_data
        self.test_data = test_data
        self.input_model = input_model
