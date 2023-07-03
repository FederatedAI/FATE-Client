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


class Statistics(Component):
    yaml_define_path = "./component_define/fate/statistics.yaml"

    def __init__(self,
                 name: str,
                 runtime_roles: List[str] = None,
                 metrics: List[str] = None,
                 bias: bool = True,
                 skip_col: List[str] = PlaceHolder(),
                 use_anonymous: bool = False,
                 train_data: ArtifactType = PlaceHolder()
                 ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(Statistics, self).__init__()
        self.name = name
        self.runtime_roles = runtime_roles
        self.metrics = metrics
        self.bias = bias
        self.skip_col = skip_col
        self.use_anonymous = use_anonymous
        self.train_data = train_data
