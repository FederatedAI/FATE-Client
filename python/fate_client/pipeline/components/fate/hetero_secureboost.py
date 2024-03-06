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


class HeteroSecureBoost(Component):
    yaml_define_path = "./component_define/fate/hetero_secureboost.yaml"

    def __init__(
        self,
        _name: str,
        runtime_parties: dict = None,
        train_data: ArtifactType = PlaceHolder(),
        validate_data: ArtifactType = PlaceHolder(),
        num_trees: int = 20,
        learning_rate: float = 0.3,
        max_depth: int = 3,
        max_bin: int = 32,
        objective: str = "binary:bce",
        num_class: int = 2,
        goss: bool = False,
        goss_start_iter: int = 0,
        top_rate: float = 0.2,
        other_rate: float = 0.1,
        l1: float = 0,
        l2: float = 0.1,
        min_impurity_split: float = 1e-2,
        min_sample_split: int = 2,
        min_leaf_node: int = 1,
        min_child_weight: float = 1,
        gh_pack: bool = True,
        split_info_pack: bool = True,
        hist_sub: bool = True,
        he_param: dict = PlaceHolder(),
        cv_param: dict = PlaceHolder(),
        train_output_data: ArtifactType = PlaceHolder(),
        output_model: ArtifactType = PlaceHolder(),
        warm_start_model: ArtifactType = PlaceHolder(),
        test_data: ArtifactType = PlaceHolder(),
        input_model: ArtifactType = PlaceHolder(),
        cv_data: ArtifactType = PlaceHolder()
    ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(HeteroSecureBoost, self).__init__()
        self._name = _name
        self.runtime_parties = runtime_parties
        self.train_data = train_data
        self.validate_data = validate_data
        self.warm_start_model = warm_start_model
        self.num_trees = num_trees
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.max_bin = max_bin
        self.objective = objective
        self.num_class = num_class
        self.l2 = l2
        self.l1 = l1
        self.goss = goss
        self.goss_start_iter = goss_start_iter
        self.top_rate = top_rate
        self.other_rate = other_rate
        self.top_rate = top_rate
        self.other_rate = other_rate
        self.min_impurity_split = min_impurity_split
        self.min_sample_split = min_sample_split
        self.min_leaf_node = min_leaf_node
        self.min_child_weight = min_child_weight
        self.gh_pack = gh_pack
        self.split_info_pack = split_info_pack
        self.hist_sub = hist_sub
        self.he_param = he_param
        self.train_output_data = train_output_data
        self.output_model = output_model
        self.test_data = test_data
        self.input_model = input_model
        self.cv_param = cv_param
        self.cv_data = cv_data
