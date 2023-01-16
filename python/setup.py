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
    "click>=7.1.2,<8.0.0",
    "poetry>=0.12",
    "pandas>=1.1.5",
    "requests>=2.24.0,<3.0.0",
    "requests_toolbelt>=0.9.1,<0.10.0",
    "ruamel.yaml>=0.16.10",
    "setuptools>=65.5.1",
    "networkx>=2.8.7",
    "pydantic",
    "ml_metadata",
]

extras_require = {
    "fate": ["pyfate"],
}
entry_points = {"console_scripts": ["fate_client = fate_client.cli:cli"]}

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
