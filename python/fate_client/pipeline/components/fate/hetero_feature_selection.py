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
from ...interface import ArtifactType


class HeteroFeatureSelection(Component):
    yaml_define_path = "./component_define/fate/hetero_feature_selection.yaml"

    def __init__(
        self,
        _name: str,
        runtime_parties: dict = None,
        method: List[str] = PlaceHolder(),
        select_col: List[str] = None,
        iv_param: dict = None,
        statistic_param: dict = None,
        manual_param: dict = None,
        keep_one: bool = True,
        use_anonymous: bool = False,
        train_data: ArtifactType = PlaceHolder(),
        test_data: ArtifactType = PlaceHolder(),
        input_model: ArtifactType = PlaceHolder(),
        input_models: List[ArtifactType] = PlaceHolder(),
    ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(HeteroFeatureSelection, self).__init__()
        self._name = _name
        self.runtime_parties = runtime_parties
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
        self.input_models = input_models
