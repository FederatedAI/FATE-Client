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
from typing import Dict, List, Union

from ..component_base import Component
from ...conf.types import PlaceHolder
from ...interface import ArtifactType


class FeatureImputation(Component):
    yaml_define_path = "./component_define/fate/feature_imputation.yaml"

    def __init__(self,
                 _name: str,
                 runtime_roles: List[str] = None,
                 method: str = PlaceHolder(),
                 col_fill_method: Dict[str, str] = None,
                 fill_const: Union[int, float] = None,
                 missing_val: list = None,
                 use_anonymous: bool = False,
                 train_data: ArtifactType = PlaceHolder(),
                 test_data: ArtifactType = PlaceHolder(),
                 input_model: ArtifactType = PlaceHolder()
                 ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(FeatureImputation, self).__init__()
        self._name = _name
        self.runtime_roles = runtime_roles
        self.method = method
        self.col_fill_method = col_fill_method
        self.fill_const = fill_const
        self.missing_val = missing_val
        self.use_anonymous = use_anonymous
        self.train_data = train_data
        self.test_data = test_data
        self.input_model = input_model
