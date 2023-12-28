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
import click

from ..utils import cli_args
from ..utils.cli_utils import load_yaml, preprocess, prettify
from fate_client.flow_sdk import FlowClient


@click.group()
@click.pass_context
def site(ctx):
    """
    \b
    -description: Site Operations

    """
    pass


@site.command("query")
@click.pass_context
def info(ctx):
    """
    \b
    -description: Querying Site Information

    \b
    -usage: flow site query
    """
    client: FlowClient = ctx.obj["client"]
    response = client.site.info()
    prettify(response)
