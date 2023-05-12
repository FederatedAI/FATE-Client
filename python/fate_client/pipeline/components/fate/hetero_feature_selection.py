#
#  Copyright 2023 The FATE Authors. All Rights Reserved.
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
from ...interface import ArtifactChannel


class HeteroFeatureSelection(Component):
    yaml_define_path = "./component_define/fate/hetero_feature_selection.yaml"

    def __init__(self,
                 name: str,
                 runtime_roles: List[str] = None,
                 method: List[str] = PlaceHolder(),
                 select_col: List[str] = None,
                 iv_param: dict = None,
                 statistic_param: dict = None,
                 manual_param: dict = None,
                 keep_one: bool = True,
                 use_anonymous: bool = False,
                 train_data: ArtifactChannel = PlaceHolder(),
                 test_data: ArtifactChannel = PlaceHolder(),
                 input_model: ArtifactChannel = PlaceHolder(),
                 input_statistic_model: ArtifactChannel = PlaceHolder(),
                 input_binning_model: ArtifactChannel = PlaceHolder()
                 ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(HeteroFeatureSelection, self).__init__()
        self.name = name
        self.runtime_roles = runtime_roles
        self.method = method
        self.select_col = select_col
        self.iv_param = iv_param
        self.statistic_param = statistic_param
        self.manual_param = manual_param
        self.keep_one = keep_one
        self.use_anonymous = use_anonymous
        self.train_data = train_data
        self.test_data = test_data
        self.input_model = input_model
        self.input_statistic_model = input_statistic_model
        self.input_binning_model = input_binning_model