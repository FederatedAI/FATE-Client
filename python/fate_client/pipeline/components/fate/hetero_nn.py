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
    FedPassArgument,
    TopModelStrategyArguments,
    SSHEArgument
)
from typing import Union, Optional, Dict, Literal


def get_config_of_default_runner(
        bottom_model: Union[TorchModule, Sequential, ModelLoader] = None,
        top_model: Union[TorchModule, Sequential, ModelLoader] = None,
        agglayer_arg: Union[FedPassArgument, SSHEArgument] = None,
        top_model_strategy_arg: Optional[TopModelStrategyArguments] = None,
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

    if top_model is not None and not isinstance(top_model, (TorchModule, Sequential, ModelLoader)):
        raise ValueError(
            f"The top model is of type {type(top_model)}, not TorchModule, Sequential, or ModelLoader. Remember to use patched_torch_hook for passing NN Modules or Optimizers."
        )

    if agglayer_arg is not None and not isinstance(agglayer_arg, (FedPassArgument, SSHEArgument)):
        raise ValueError(
            f"The agglayer_arg_conf is of type {type(agglayer_arg)}, not StdAggLayerArgument or FedPassArgument. "
        )

    if top_model_strategy_arg is not None and not isinstance(top_model_strategy_arg, TopModelStrategyArguments):
        raise ValueError(
            f"The top_model_strategy_arg_conf is of type {type(top_model_strategy_arg)}, not TopModelStrategyArguments. "
        )

    runner_conf['bottom_model_conf'] = bottom_model.to_dict() if bottom_model is not None else None
    runner_conf['top_model_conf'] = top_model.to_dict() if top_model is not None else None
    runner_conf['agglayer_arg_conf'] = agglayer_arg.to_dict() if agglayer_arg is not None else None
    runner_conf['top_model_strategy_arg_conf'] = top_model_strategy_arg.to_dict() if top_model_strategy_arg is not None else None

    return runner_conf


class HeteroNN(Component):
    yaml_define_path = "./component_define/fate/hetero_nn.yaml"

    def __init__(
        self,
        _name: str,
        runtime_parties: dict = None,
        runner_module: str = PlaceHolder(),
        runner_class: str = PlaceHolder(),
        runner_conf: dict = PlaceHolder(),
        source: str = PlaceHolder(),
        train_data: ArtifactType = PlaceHolder(),
        validate_data: ArtifactType = PlaceHolder(),
        test_data: ArtifactType = PlaceHolder(),
        warm_start_model: ArtifactType = PlaceHolder(),
        input_model: ArtifactType = PlaceHolder(),
    ):

        inputs = locals()
        self._process_init_inputs(inputs)
        super(HeteroNN, self).__init__()
        self._name = _name
        self.runtime_parties = runtime_parties
        self.runner_module = runner_module
        self.runner_class = runner_class
        self.runner_conf = runner_conf
        self.source = source
        self.train_data = train_data
        self.validate_data = validate_data
        self.test_data = test_data
        self.warm_start_model = warm_start_model
        self.input_model = input_model