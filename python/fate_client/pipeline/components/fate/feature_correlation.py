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


class FeatureCorrelation(Component):
    yaml_define_path = "./component_define/fate/feature_correlation.yaml"

    def __init__(
            self,
            _name: str,
            runtime_parties: dict = None,
            calc_local_vif: bool = True,
            local_only: bool = False,
            skip_col: List[str] = PlaceHolder(),
            use_anonymous: bool = False,
            input_data: ArtifactType = PlaceHolder(),
    ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(FeatureCorrelation, self).__init__()
        self._name = _name
        self.runtime_parties = runtime_parties
        self.local_only = local_only
        self.calc_local_vif = calc_local_vif
        self.skip_col = skip_col
        self.use_anonymous = use_anonymous
        self.input_data = input_data
