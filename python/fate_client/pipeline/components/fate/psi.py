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
from ...conf.types import PlaceHolder
from ..component_base import Component
from ...interface import ArtifactType


class PSI(Component):
    yaml_define_path = "./component_define/fate/psi.yaml"

    def __init__(
        self,
        _name: str,
        runtime_parties: dict = None,
        input_data: ArtifactType = PlaceHolder(),
        protocol: str = PlaceHolder(),
        curve_type: str = PlaceHolder(),
    ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(PSI, self).__init__()
        self._name = _name
        self.runtime_parties = runtime_parties
        self.input_data = input_data
        self.protocol = protocol
        self.curve_type = curve_type
