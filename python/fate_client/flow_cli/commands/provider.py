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
from ..utils.cli_utils import prettify, preprocess
from fate_client.flow_sdk import FlowClient


@click.group()
@click.pass_context
def provider(ctx):
    """
    \b
    -description: Provider Operations
    """
    pass


@provider.command("register")
@cli_args.CONF_PATH
@click.pass_context
def register(ctx, **kwargs):
    """
    \b
    -description: register provider

    \b
    -usage: flow provider register -c examples/provider/register.json

    """
    config_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.provider.register(**config_data)
    prettify(response)


@provider.command("query")
@cli_args.NAME
@cli_args.DEVICE
@cli_args.VERSION
@cli_args.PROVIDER_NAME
@click.pass_context
def query(ctx, **kwargs):
    """
    \b
    -description: Filtering Providers Based on Conditions

    \b
    -usage: flow provider query --name fate

    """
    client: FlowClient = ctx.obj["client"]
    response = client.provider.query(**kwargs)
    prettify(response)


@provider.command("delete")
@cli_args.NAME
@cli_args.DEVICE
@cli_args.VERSION
@cli_args.PROVIDER_NAME
@click.pass_context
def delete(ctx, **kwargs):
    """
    \b
    -description: Delete Providers Based on Filtering Conditions.

    \b
    -usage: flow provider delete -n xxx

    """
    client: FlowClient = ctx.obj["client"]
    response = client.provider.delete(**kwargs)
    prettify(response)





