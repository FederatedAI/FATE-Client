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
from typing import Dict
from ..conf.types import InputArtifactType, Stage
from ..entity.component_structures import ArtifactSpec


class ComponentStageSchedule(object):
    @classmethod
    def get_stage(cls, input_artifacts: Dict[str, Dict[str, ArtifactSpec]], default_stage=None):
        """
        possible:
            train_data, validate_data: stage = train
            test_data: stage = predict
            data: stage = default
            train_data & input_model: stage = train
            test_data & input_model: stage = train
        """
        task_stage = None
        for input_artifact_type in InputArtifactType.types():
            if input_artifact_type not in input_artifacts:
                continue
            artifacts = input_artifacts[input_artifact_type]
            for input_key, artifact in artifacts.items():
                stage = set(artifact.stages)
                if task_stage is None:
                    task_stage = stage
                else:
                    task_stage &= stage

        if not task_stage:
            return default_stage

        if len(task_stage) == 1:
            return list(task_stage)[0]

        """
        multiple stage, try to infer from data input artifacts
        """
        data_artifacts = input_artifacts[InputArtifactType.DATA]
        data_type = 0
        for data_key, artifact in data_artifacts.items():
            if data_key.find("train") != -1:
                data_type |= 1
            elif data_key.find("validate") != -1:
                data_type |= 2
            elif data_key.find("test") != -1:
                data_type |= 4
            else:
                data_type |= 8

        if data_type & 1:
            return Stage.TRAIN
        elif data_type & 4:
            return Stage.PREDICT
        else:
            return Stage.DEFAULT
