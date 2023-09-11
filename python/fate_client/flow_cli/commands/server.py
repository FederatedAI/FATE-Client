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
from ..utils.cli_utils import preprocess, prettify
from fate_client.flow_sdk import FlowClient


@click.group()
@click.pass_context
def server(ctx):
    """
    \b
    -description: Third-party Service Related Operations
    """
    pass


@server.command("info")
@click.pass_context
def flow_server_info(ctx):
    """
    -description: Fetching Current FATE FLow server (Cluster) Information

    \b
    -usage: flow server info
    """
    client: FlowClient = ctx.obj["client"]
    response = client.service.get_fateflow_info()
    prettify(response)
