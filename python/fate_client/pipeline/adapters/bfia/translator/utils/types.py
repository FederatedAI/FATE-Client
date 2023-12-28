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
#

def get_source_type(type_keyword):
    data_keywords = ["data", "dataset", "training_set", "test_set", "validate_set"]
    model_keywords = ["model"]
    for data_keyword in data_keywords:
        if data_keyword in type_keyword:
            return "data"

    for model_keyword in model_keywords:
        if model_keyword in type_keyword:
            return "model"

    return "metric"
