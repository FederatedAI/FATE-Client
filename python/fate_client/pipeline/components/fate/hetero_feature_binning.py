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


class HeteroFeatureBinning(Component):
    yaml_define_path = "./component_define/fate/hetero_feature_binning.yaml"

    def __init__(self,
                 name: str,
                 runtime_roles: List[str] = None,
                 method: str = PlaceHolder(),
                 split_pt_dict: dict = None,
                 n_bins: int = None,
                 bin_col: List[str] = None,
                 bin_idx: List[int] = None,
                 category_col: List[str] = None,
                 category_idx: List[int] = None,
                 use_anonymous: bool = False,
                 transform_method: str = None,
                 skip_metrics: List[str] = None,
                 local_only: bool = False,
                 error_rate: float = 1e-3,
                 adjustment_factor: float = 0.5,
                 train_data: ArtifactChannel = PlaceHolder(),
                 test_data: ArtifactChannel = PlaceHolder(),
                 input_model: ArtifactChannel = PlaceHolder()
                 ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(HeteroFeatureBinning, self).__init__()
        self.name = name
        self.runtime_roles = runtime_roles
        self.method = method
        self.split_pt_dict = split_pt_dict
        self.n_bins = n_bins
        self.bin_col = bin_col
        self.bin_idx = bin_idx
        self.category_col = category_col
        self.category_idx = category_idx
        self.use_anonymous = use_anonymous
        self.transform_method = transform_method
        self.skip_metrics = skip_metrics
        self.local_only = local_only
        self.error_rate = error_rate
        self.adjustment_factor = adjustment_factor
        self.train_data = train_data
        self.test_data = test_data
        self.input_model = input_model
