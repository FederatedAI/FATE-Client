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


class HeteroFeatureBinning(Component):
    yaml_define_path = "./component_define/fate/hetero_feature_binning.yaml"

    def __init__(
        self,
        _name: str,
        runtime_roles: List[str] = None,
        method: str = PlaceHolder(),
        n_bins: int = None,
        split_pt_dict: dict = None,
        bin_col: List[str] = None,
        bin_idx: List[int] = None,
        category_col: List[str] = None,
        category_idx: List[int] = None,
        use_anonymous: bool = False,
        transform_method: str = None,
        skip_metrics: bool = False,
        local_only: bool = False,
        relative_error: float = 1e-6,
        adjustment_factor: float = 0.5,
        he_param: dict = PlaceHolder(),
        train_data: ArtifactType = PlaceHolder(),
        test_data: ArtifactType = PlaceHolder(),
        input_model: ArtifactType = PlaceHolder(),
    ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(HeteroFeatureBinning, self).__init__()
        self._name = _name
        self.runtime_roles = runtime_roles
        self.method = method
        self.n_bins = n_bins
        self.split_pt_dict = split_pt_dict
        self.bin_col = bin_col
        self.bin_idx = bin_idx
        self.category_col = category_col
        self.category_idx = category_idx
        self.transform_method = transform_method
        self.skip_metrics = skip_metrics
        self.local_only = local_only
        self.relative_error = relative_error
        self.adjustment_factor = adjustment_factor
        self.use_anonymous = use_anonymous
        self.train_data = train_data
        self.test_data = test_data
        self.input_model = input_model
        self.he_param = he_param
