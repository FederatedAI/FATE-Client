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
from ...conf.types import PlaceHolder
from ..component_base import Component
from ...interface import ArtifactType


class DataFrameIOTest(Component):
    yaml_define_path = "./component_define/fate/dataframe_io_test.yaml"

    def __init__(
        self,
        _name: str,
        dataframe_input: ArtifactType = PlaceHolder(),
        dataframe_inputs: ArtifactType = PlaceHolder(),
    ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(DataFrameIOTest, self).__init__()
        self._name = _name
        self.dataframe_input = dataframe_input
        self.dataframe_inputs = dataframe_inputs
