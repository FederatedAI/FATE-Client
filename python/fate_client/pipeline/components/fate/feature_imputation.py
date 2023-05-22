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
from typing import List, Union

from ..component_base import Component
from ...conf.types import PlaceHolder
from ...interface import ArtifactChannel


class FeatureImputation(Component):
    yaml_define_path = "./component_define/fate/feature_imputation.yaml"

    def __init__(self,
                 name: str,
                 runtime_roles: List[str] = None,
                 missing_fill_method: str = PlaceHolder(),
                 col_missing_fill_method: Union[str, dict] = None,
                 missing_value: Union[int, float, List[int], List[float]] = None,
                 designated_fill_value: Union[int, float] = 0,
                 imputation_col: List[str] = None,
                 imputation_idx: List[int] = None,
                 use_anonymous: bool = False,
                 train_data: ArtifactChannel = PlaceHolder(),
                 test_data: ArtifactChannel = PlaceHolder(),
                 input_model: ArtifactChannel = PlaceHolder()
                 ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(FeatureImputation, self).__init__()
        self.name = name
        self.runtime_roles = runtime_roles
        self.missing_fill_method = missing_fill_method
        self.col_missing_fill_method = col_missing_fill_method
        self.missing_value = missing_value
        self.designated_fill_value = designated_fill_value
        self.imputation_col = imputation_col
        self.imputation_idx = imputation_idx
        self.use_anonymous = use_anonymous
        self.train_data = train_data
        self.test_data = test_data
        self.input_model = input_model
