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
from typing import List

from ..component_base import Component
from ...conf.types import PlaceHolder


class Reader(Component):
    yaml_define_path = "./component_define/fate/reader.yaml"

    def __init__(
        self,
        _name: str,
        runtime_parties: dict = None,
        namespace: str = PlaceHolder(),
        name: str = PlaceHolder()
    ):
        inputs = locals()
        self._process_init_inputs(inputs)
        super(Reader, self).__init__()
        self._name = _name
        self.runtime_parties = runtime_parties
        self.name = name
        self.namespace = namespace
