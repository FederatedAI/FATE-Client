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
from fate_client.pipeline.conf.types import PlaceHolder
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
from typing import Union
from fate_client.pipeline.components.fate.nn.algo_params import (
    TrainingArguments,
    FedArguments,
)
from typing import Literal
from ...conf.types import PlaceHolder
from ..component_base import Component
from ...interface import ArtifactType


def get_config_of_default_runner(
    algo: str = "fedavg",
    model: Union[TorchModule, Sequential, ModelLoader] = None,
    optimizer: Union[TorchOptimizer, Loader] = None,
    loss: Union[TorchModule, CustFuncLoader] = None,
    training_args: TrainingArguments = None,
    fed_args: FedArguments = None,
    dataset: DatasetLoader = None,
    data_collator: CustFuncLoader = None,
    tokenizer: CustFuncLoader = None,
    task_type: Literal["binary", "multi", "regression", "others"] = "binary",
):
    if model is not None and not isinstance(
        model, (TorchModule, Sequential, ModelLoader)
    ):
        raise ValueError(
            f"The model is of type {type(model)}, not TorchModule, Sequential, or ModelLoader. Remember to use patched_torch_hook for passing NN Modules or Optimizers."
        )

    if optimizer is not None and not isinstance(optimizer, (TorchOptimizer, Loader)):
        raise ValueError(
            f"The optimizer is of type {type(optimizer)}, not TorchOptimizer or Loader. Remember to use patched_torch_hook for passing NN Modules or Optimizers."
        )

    if loss is not None and not isinstance(loss, (TorchModule, CustFuncLoader)):
        raise ValueError(
            f"The loss function is of type {type(loss)}, not TorchModule or CustFuncLoader."
        )

    if training_args is not None and not isinstance(training_args, TrainingArguments):
        raise ValueError(
            f"Training arguments are of type {type(training_args)}, not TrainingArguments."
        )

    if fed_args is not None and not isinstance(fed_args, FedArguments):
        raise ValueError(
            f"Federation arguments are of type {type(fed_args)}, not FedArguments."
        )

    if dataset is not None and not isinstance(dataset, DatasetLoader):
        raise ValueError(f"The dataset is of type {type(dataset)}, not DatasetLoader.")

    if data_collator is not None and not isinstance(data_collator, CustFuncLoader):
        raise ValueError(
            f"The data collator is of type {type(data_collator)}, not CustFuncLoader."
        )

    if tokenizer is not None and not isinstance(tokenizer, CustFuncLoader):
        raise ValueError(
            f"The tokenizer is of type {type(tokenizer)}, not CustFuncLoader."
        )

    if task_type not in ["binary", "multi", "regression", "others"]:
        raise ValueError(
            f"The task type is {task_type}, not 'binary', 'multi', 'regression', 'others'."
        )

    runner_conf = {
        "algo": algo,
        "model_conf": model.to_dict() if model is not None else None,
        "optimizer_conf": optimizer.to_dict() if optimizer is not None else None,
        "loss_conf": loss.to_dict() if loss is not None else None,
        "training_args_conf": training_args.to_dict()
        if training_args is not None
        else None,
        "fed_args_conf": fed_args.to_dict() if fed_args is not None else None,
        "dataset_conf": dataset.to_dict() if dataset is not None else None,
        "data_collator_conf": data_collator.to_dict()
        if data_collator is not None
        else None,
        "tokenizer_conf": tokenizer.to_dict() if tokenizer is not None else None,
        "task_type": task_type,
    }

    return runner_conf


class HomoNN(Component):
    yaml_define_path = "./component_define/fate/homo_nn.yaml"

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
        super(HomoNN, self).__init__()
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
