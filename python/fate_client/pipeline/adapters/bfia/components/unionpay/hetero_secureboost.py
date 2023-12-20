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


class HeteroSecureBoost(Component):
    yaml_define_path = "./adapters/bfia/component_define/unionpay/hetero_secureboost.yaml"

    def __init__(
        self,
        _name: str,
        runtime_parties: dict = None,
        id: str = PlaceHolder(),
        label: str = PlaceHolder(),
        objective_param: str = PlaceHolder(),
        learning_rate: float = 0.15,
        num_trees: int = 5,
        subsample_feature_rate: float = 1.0,
        n_iter_no_change: bool = True,
        tol: float = 0.0001,
        bin_num: int = 32,
        predict_param: str = PlaceHolder(),
        cv_param: str = PlaceHolder(),
        metrics: str = PlaceHolder(),
        early_stop: str = PlaceHolder(),
        early_stopping_rounds: int = PlaceHolder(),
        tree_param: str = PlaceHolder(),
        train_data: ArtifactType = PlaceHolder()
    ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(HeteroSecureBoost, self).__init__()
        self._name = _name
        self.runtime_parties = runtime_parties
        self.id = id
        self.label = label
        self.objective_param = objective_param
        self.learning_rate = learning_rate
        self.num_trees = num_trees
        self.subsample_feature_rate = subsample_feature_rate
        self.n_iter_no_change = n_iter_no_change
        self.tol = tol
        self.bin_num = bin_num
        self.predict_param = predict_param
        self.cv_param = cv_param
        self.metrics = metrics
        self.tree_param = tree_param
        self.early_stop = early_stop
        self.train_data = train_data
