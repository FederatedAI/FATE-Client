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
from fate_client.pipeline.components.component_base import Component
from fate_client.pipeline.conf.types import PlaceHolder
from fate_client.pipeline.interface import ArtifactType


class HeteroLR(Component):
    yaml_define_path = "./adapters/bfia/component_define/unionpay/hetero_lr.yaml"

    def __init__(
        self,
        _name: str,
        runtime_parties: dict = None,
        id: str = PlaceHolder(),
        label: str = PlaceHolder(),
        penalty: str = PlaceHolder(),
        tol: float = PlaceHolder(),
        alpha: float = PlaceHolder(),
        optimizer: str = PlaceHolder(),
        batch_size: int = PlaceHolder(),
        learning_rate: float = PlaceHolder(),
        init_param: str = PlaceHolder(),
        max_iter: int = PlaceHolder(),
        early_stop: str = PlaceHolder(),
        train_data: ArtifactType = PlaceHolder()
    ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(HeteroLR, self).__init__()
        self._name = _name
        self.runtime_parties = runtime_parties
        self.id = id
        self.label = label
        self.penalty = penalty
        self.tol = tol
        self.alpha = alpha
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.init_param = init_param
        self.max_iter = max_iter
        self.early_stop = early_stop
        self.train_data = train_data
