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
                 setup_module: str = PlaceHolder(),
                 setup_class: str = PlaceHolder(),
                 setup_conf: dict = PlaceHolder(),
                 source: str = PlaceHolder(),
                 train_data: ArtifactChannel = PlaceHolder(),
                 validate_data: ArtifactChannel = PlaceHolder(),
                 ):
        
        inputs = locals()
        self._process_init_inputs(inputs)
        super(_HomoNN, self).__init__()
        self.name = name
        self.runtime_roles = runtime_roles
        self.setup_module = setup_module
        self.setup_class = setup_class
        self.setup_conf = setup_conf
        self.source = source
        self.train_data = train_data
        self.validate_data = validate_data


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
                 ):
        
        # Type Checking
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
        
        super(HomoNN, self).__init__(name=name, 
                                     runtime_roles=runtime_roles,
                                     algo=algo,
                                     model=model,
                                     optimizer=optimizer,
                                     loss=loss,
                                     training_args=training_args,
                                     fed_args=fed_args,
                                     dataset=dataset,
                                     data_collator=data_collator)




class CustomSetupHomoNN(_HomoNN):

    def __init__(self,
        name: str,
        runtime_roles: List[str] = None,
        setup_module: str = PlaceHolder(),
        setup_class: str = PlaceHolder(),
        setup_conf: dict = PlaceHolder(),
        source: str = PlaceHolder(),
        train_data: ArtifactChannel = PlaceHolder(),
        validate_data: ArtifactChannel = PlaceHolder(),
        ):

        super(CustomSetupHomoNN, self).__init__(name, runtime_roles, setup_module, 
                                                setup_class, setup_conf, source, train_data, validate_data)