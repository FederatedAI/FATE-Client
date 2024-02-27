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
from typing import List, Literal
from ...conf.types import PlaceHolder
from ..component_base import Component
from ...interface import ArtifactType


class Evaluation(Component):
    yaml_define_path = "./component_define/fate/evaluation.yaml"

    def __init__(
        self,
        _name: str,
        runtime_parties: dict = None,
        default_eval_setting: Literal["binary", "multi", "regression"] = PlaceHolder(),
        metrics: List[str] = None,
        predict_column_name: str = None,
        label_column_name: str = None,
        input_datas: ArtifactType = PlaceHolder(),
    ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(Evaluation, self).__init__()
        self._name = _name
        self.runtime_parties = runtime_parties
        self.input_datas = input_datas
        self.default_eval_setting = default_eval_setting
        self.metrics = metrics
        self.predict_column_name = predict_column_name
        self.label_column_name = label_column_name
