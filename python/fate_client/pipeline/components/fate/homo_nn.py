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
from fate_client.pipeline.interface import ArtifactChannel
from fate_client.pipeline.components.fate.nn.loader import Loader, ModelLoader, CustFuncLoader, DatasetLoader
from fate_client.pipeline.components.fate.nn.fate_torch.base import FateTorch, FateTorchOptimizer, Sequential
from typing import Union
from fate_client.pipeline.components.fate.nn.algo_params import TrainingArguments, FedArguments
from ...conf.types import PlaceHolder
from ..component_base import Component
from ...interface import ArtifactChannel


class _HomoNN(Component):
    
    yaml_define_path = "./component_define/fate/homo_nn.yaml"

    def __init__(self,
                 name: str,
                 runtime_roles: List[str] = None,
                 runner_module: str = PlaceHolder(),
                 runner_class: str = PlaceHolder(),
                 runner_conf: dict = PlaceHolder(),
                 source: str = PlaceHolder(),
                 train_data: ArtifactChannel = PlaceHolder(),
                 validate_data: ArtifactChannel = PlaceHolder(),
                 test_data: ArtifactChannel = PlaceHolder(),
                 input_model: ArtifactChannel = PlaceHolder(),
                 ):
        
        inputs = locals()
        self._process_init_inputs(inputs)
        super(_HomoNN, self).__init__()
        self.name = name
        self.runtime_roles = runtime_roles
        self.runner_module = runner_module
        self.runner_class = runner_class
        self.runner_conf = runner_conf
        self.source = source
        self.train_data = train_data
        self.validate_data = validate_data
        self.test_data = test_data
        self.input_model = input_model
        

class HomoNN(_HomoNN):
    
    def __init__(self, 
                 name: str,
                 runtime_roles: List[str] = None,
                 algo: str = 'fedavg',
                 model: Union[FateTorch, Sequential, ModelLoader] = None,
                 optimizer: Union[FateTorchOptimizer, Loader] = None,
                 loss: Union[FateTorch, CustFuncLoader] = None,
                 training_args: TrainingArguments = None,
                 fed_args: FedArguments = None,
                 dataset: DatasetLoader = None,
                 data_collator: CustFuncLoader = None,
                 tokenizer: CustFuncLoader = None,
                 train_data: ArtifactChannel = PlaceHolder(),
                 validate_data: ArtifactChannel = PlaceHolder(),
                 test_data: ArtifactChannel = PlaceHolder(),
                 input_model: ArtifactChannel = PlaceHolder()
                 ):
        
        if model is not None and not isinstance(model, (FateTorch, Sequential, ModelLoader)):
            raise ValueError(f'The model is of type {type(model)}, not FateTorch, Sequential, or ModelLoader. Remember to use fate_torch_hook for passing NN Modules or Optimizers.')
        
        if optimizer is not None and not isinstance(optimizer, (FateTorchOptimizer, Loader)):
            raise ValueError(f'The optimizer is of type {type(optimizer)}, not FateTorchOptimizer or Loader. Remember to use fate_torch_hook for passing NN Modules or Optimizers.')
        
        if loss is not None and not isinstance(loss, (FateTorch, CustFuncLoader)):
            raise ValueError(f'The loss function is of type {type(loss)}, not FateTorch or CustFuncLoader.')
        
        if training_args is not None and not isinstance(training_args, TrainingArguments):
            raise ValueError(f'Training arguments are of type {type(training_args)}, not TrainingArguments.')
        
        if fed_args is not None and not isinstance(fed_args, FedArguments):
            raise ValueError(f'Federation arguments are of type {type(fed_args)}, not FedArguments.')
        
        if dataset is not None and not isinstance(dataset, DatasetLoader):
            raise ValueError(f'The dataset is of type {type(dataset)}, not DatasetLoader.')
        
        if data_collator is not None and not isinstance(data_collator, CustFuncLoader):
            raise ValueError(f'The data collator is of type {type(data_collator)}, not CustFuncLoader.')

        if tokenizer is not None and not isinstance(tokenizer, CustFuncLoader):
            raise ValueError(f'The tokenizer is of type {type(tokenizer)}, not CustFuncLoader.')

        runner_conf = {
            'algo': algo,
            'model_conf': model.to_dict() if model is not None else None,
            'optimizer_conf': optimizer.to_dict() if optimizer is not None else None,
            'loss_conf': loss.to_dict() if loss is not None else None,
            'training_args_conf': training_args.to_dict() if training_args is not None else None,
            'fed_args_conf': fed_args.to_dict() if fed_args is not None else None,
            'dataset_conf': dataset.to_dict() if dataset is not None else None,
            'data_collator_conf': data_collator.to_dict() if data_collator is not None else None,
            'tokenizer_conf': tokenizer.to_dict() if tokenizer is not None else None
        }

        super(HomoNN, self).__init__(name=name, 
                                     runtime_roles=runtime_roles,
                                     train_data=train_data,
                                     validate_data=validate_data,
                                     runner_conf=runner_conf,
                                     runner_module='fate_runner',
                                     runner_class='Faterunner',
                                     test_data=test_data,
                                     input_model=input_model
                                     )


class CustomrunnerHomoNN(_HomoNN):

    def __init__(self,
        name: str,
        runtime_roles: List[str] = None,
        runner_module: str = PlaceHolder(),
        runner_class: str = PlaceHolder(),
        runner_conf: dict = PlaceHolder(),
        source: str = PlaceHolder(),
        train_data: ArtifactChannel = PlaceHolder(),
        validate_data: ArtifactChannel = PlaceHolder(),
        test_data: ArtifactChannel = PlaceHolder(),
        input_model: ArtifactChannel = PlaceHolder()
        ):

        super(CustomrunnerHomoNN, self).__init__(name, runtime_roles, runner_module, 
                                                runner_class, runner_conf, source, train_data, validate_data, test_data, input_model)