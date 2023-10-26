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
from ...conf.types import PlaceHolder
from ..component_base import Component
from ...interface import ArtifactType
from fate_client.pipeline.components.fate.nn.common_utils import get_config_of_default_runner as _get_config_of_default_runner
from fate_client.pipeline.components.fate.nn.loader import (
    Loader,
    ModelLoader,
    CustFuncLoader,
    DatasetLoader,
)
from fate_client.pipeline.components.fate.nn.torch.base import (
    TorchModule,
    TorchOptimizer,
    Sequential,
)
from fate_client.pipeline.components.fate.nn.algo_params import (
    TrainingArguments,
)
from typing import Union, Optional, Dict, Literal


def get_config_of_default_runner(
        bottom_model: Union[TorchModule, Sequential, ModelLoader] = None,
        agg_layer: Union[ModelLoader] = None,
        top_model: Union[TorchModule, Sequential, ModelLoader] = None,
        optimizer: Union[TorchOptimizer, Loader] = None,
        loss: Union[TorchModule, CustFuncLoader] = None,
        training_args: TrainingArguments = None,
        dataset: DatasetLoader = None,
        data_collator: CustFuncLoader = None,
        tokenizer: CustFuncLoader = None,
        task_type: Literal["binary", "multi", "regression", "others"] = "binary"):

    runner_conf = _get_config_of_default_runner(
        optimizer, loss, training_args, dataset, data_collator, tokenizer, task_type
    )

    if bottom_model is not None and not isinstance(bottom_model, (TorchModule, Sequential, ModelLoader)):
        raise ValueError(
            f"The bottom model is of type {type(bottom_model)}, not TorchModule, Sequential, or ModelLoader. Remember to use patched_torch_hook for passing NN Modules or Optimizers."
        )

    if agg_layer is not None and not isinstance(agg_layer, ModelLoader):
        raise ValueError(
            f"The agg layer is of type {type(agg_layer)}, not ModelLoader. Remember to use patched_torch_hook for passing NN Modules or Optimizers."
        )

    if top_model is not None and not isinstance(top_model, (TorchModule, Sequential, ModelLoader)):
        raise ValueError(
            f"The top model is of type {type(top_model)}, not TorchModule, Sequential, or ModelLoader. Remember to use patched_torch_hook for passing NN Modules or Optimizers."
        )

    runner_conf['bottom_model_conf'] = bottom_model.to_dict() if bottom_model is not None else None
    runner_conf['agg_layer_conf'] = agg_layer.to_dict() if agg_layer is not None else None
    runner_conf['top_model_conf'] = top_model.to_dict() if top_model is not None else None

    return runner_conf


class HeteroNN(Component):
    yaml_define_path = "./component_define/fate/hetero_nn.yaml"

    def __init__(
        self,
        _name: str,
        runtime_roles: List[str] = None,
        runner_module: str = PlaceHolder(),
        runner_class: str = PlaceHolder(),
        runner_conf: dict = PlaceHolder(),
        source: str = PlaceHolder(),
        train_data: ArtifactType = PlaceHolder(),
        validate_data: ArtifactType = PlaceHolder(),
        test_data: ArtifactType = PlaceHolder(),
        train_model_input: ArtifactType = PlaceHolder(),
        predict_model_input: ArtifactType = PlaceHolder(),
    ):

        inputs = locals()
        self._process_init_inputs(inputs)
        super(HeteroNN, self).__init__()
        self._name = _name
        self.runtime_roles = runtime_roles
        self.runner_module = runner_module
        self.runner_class = runner_class
        self.runner_conf = runner_conf
        self.source = source
        self.train_data = train_data
        self.validate_data = validate_data
        self.test_data = test_data
        self.train_model_input = train_model_input
        self.predict_model_input = predict_model_input