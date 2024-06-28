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
from fate_client.pipeline.components.fate.nn.common_utils import (get_config_of_default_runner
                                                                  as _get_config_of_default_runner)
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
    task_type: Literal["binary", "multi", "regression", "causal_lm", "others"] = "binary",
):

    if model is not None and not isinstance(
        model, (TorchModule, Sequential, ModelLoader)
    ):
        raise ValueError(
            f"The model is of type {type(model)}, not TorchModule, Sequential, or ModelLoader. Remember to use patched_torch_hook for passing NN Modules or Optimizers."
        )

    if fed_args is not None and not isinstance(fed_args, FedArguments):
        raise ValueError(
            f"Federation arguments are of type {type(fed_args)}, not FedArguments."
        )

    runner_conf = _get_config_of_default_runner(
        optimizer, loss, training_args, dataset, data_collator, tokenizer, task_type
    )
    runner_conf['algo'] = algo
    runner_conf['model_conf'] = model.to_dict() if model is not None else None
    runner_conf['fed_args_conf'] = fed_args.to_dict() if fed_args is not None else None

    return runner_conf


def get_config_of_seq2seq_runner(
    algo: str = "fedavg",
    model: Union[TorchModule, Sequential, ModelLoader] = None,
    optimizer: Union[TorchOptimizer, Loader] = None,
    training_args: TrainingArguments = None,
    fed_args: FedArguments = None,
    dataset: DatasetLoader = None,
    data_collator: CustFuncLoader = None,
    tokenizer: CustFuncLoader = None,
    task_type: Literal["causal_lm", "others"] = "causal_lm",
    save_trainable_weights_only: bool = False,
):
    runner_conf = get_config_of_default_runner(
        algo=algo,
        model=model,
        optimizer=optimizer,
        training_args=training_args,
        fed_args=fed_args,
        dataset=dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
        task_type=task_type
    )
    runner_conf.pop("loss_conf")
    runner_conf["save_trainable_weights_only"] = save_trainable_weights_only

    return runner_conf


def get_conf_of_ot_runner(
    model: Union[TorchModule, Sequential, ModelLoader] = None,
    optimizer: Union[TorchOptimizer, Loader] = None,
    training_args: TrainingArguments = None,
    fed_args: FedArguments = None,
    dataset: DatasetLoader = None,
    data_collator: CustFuncLoader = None,
    tokenizer: CustFuncLoader = None,
    task_type: Literal["causal_lm", "others"] = "causal_lm",
    save_trainable_weights_only: bool = False,  
    aggregate_model: bool = False
):
    runner_conf = get_config_of_default_runner(
        algo='ot',  # offsite-tuning
        model=model,
        optimizer=optimizer,
        training_args=training_args,
        fed_args=fed_args,
        dataset=dataset,
        data_collator=data_collator,
        tokenizer=tokenizer,
        task_type=task_type
    )
    runner_conf.pop("loss_conf")
    runner_conf["save_trainable_weights_only"] = save_trainable_weights_only
    runner_conf["aggregate_model"] = aggregate_model

    return runner_conf


def get_config_of_fedmkt_runner(
    model: Union[TorchModule, Sequential, ModelLoader] = None,
    optimizer: Union[TorchOptimizer, Loader] = None,
    training_args: TrainingArguments = None,
    fed_args: FedArguments = None,
    pub_dataset: DatasetLoader = None,
    priv_dataset: DatasetLoader = None,
    data_collator: CustFuncLoader = None,
    tokenizer: CustFuncLoader = None,
    llm_tokenizer: CustFuncLoader = None,
    slm_tokenizers: List[CustFuncLoader] = None,
    llm_to_slm_vocab_mapping_path: str = None,
    slm_to_llm_vocab_mapping_paths: List[str] = None,
    task_type: Literal["causal_lm", "others"] = "causal_lm",
    save_trainable_weights_only: bool = False,
    pub_dataset_path: str = None,
):
    runner_conf = {
        "algo": "fedmkt",
        "model_conf": model.to_dict() if model is not None else None,
        "optimizer_conf": optimizer.to_dict() if optimizer is not None else None,
        "training_args_conf": training_args.to_dict() if training_args is not None else None,
        "fed_args_conf": fed_args.to_dict() if fed_args is not None else None,
        "pub_dataset_conf": pub_dataset.to_dict() if pub_dataset is not None else None,
        "priv_dataset_conf": priv_dataset.to_dict() if priv_dataset is not None else None,
        "data_collator_conf": data_collator.to_dict() if data_collator is not None else None,
        "tokenizer_conf": tokenizer.to_dict() if tokenizer is not None else None,
        "llm_tokenizer_conf": llm_tokenizer.to_dict() if llm_tokenizer is not None else None,
        "llm_to_slm_vocab_mapping_path": llm_to_slm_vocab_mapping_path,
        "slm_to_llm_vocab_mapping_paths": slm_to_llm_vocab_mapping_paths,
        "task_type": task_type,
        "save_trainable_weights_only": save_trainable_weights_only,
        "pub_dataset_path": pub_dataset_path
    }

    slm_tokenizers_conf = None
    if slm_tokenizers:
        slm_tokenizers_conf = [slm_tokenizer.to_dict() for slm_tokenizer in slm_tokenizers]

    runner_conf["slm_tokenizers_conf"] = slm_tokenizers_conf

    return runner_conf


class HomoNN(Component):
    yaml_define_path = "./component_define/fate/homo_nn.yaml"

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
        super(HomoNN, self).__init__()
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
