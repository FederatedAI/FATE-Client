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
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import fate_client

packages = find_packages(".")
package_data = {"": ["*"]}

install_requires = [
    "click",
    "pandas",
    "psutil",
    "requests",
    "requests_toolbelt",
    "ruamel.yaml",
    "setuptools",
    "networkx",
    "pydantic",
]

extras_require = {
    "fate": ["pyfate==2.0.0b0"],
    "fate_flow": ["fate_flow==2.0.0b0"]
}
entry_points = {"console_scripts": ["flow = fate_client.flow_cli.flow:flow_cli",
                                    "pipeline = fate_client.pipeline.pipeline_cli:pipeline_group"]}

setup_kwargs = {
    "name": "fate-client",
    "version": fate_client.__version__,
    "description": "Clients for FATE, supply pipeline this version",
    "long_description_content_type": "text/markdown",
    "long_description": "Clients for FATE, supply pipeline this version",
    "author": "FederatedAI",
    "author_email": "contact@FedAI.org",
    "maintainer": None,
    "maintainer_email": None,
    "url": "https://fate.fedai.org/",
    "packages": packages,
    "include_package_data": True,
    "install_requires": install_requires,
    "extras_require": extras_require,
    "entry_points": entry_points,
    "python_requires": ">=3.8",
}


setup(**setup_kwargs)
