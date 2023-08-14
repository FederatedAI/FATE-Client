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


@click.group(short_help="FATE Flow Server Operations")
@click.pass_context
def server(ctx):
    """
    \b
    Provides numbers of component operational commands, including metrics, parameters and etc.
    For more details, please check out the help text.
    """
    pass


@server.command("get-server", short_help="Get Server Command")
@click.pass_context
def get_server(ctx):
    """
    - DESCRIPTION:

    \b
    - USAGE:
        flow server  fate-flow
    """
    client: FlowClient = ctx.obj["client"]
    response = client.service.get_server()
    prettify(response)


@server.command("query-all", short_help="Query All Server Command")
@click.pass_context
def get_server(ctx):
    """
    - DESCRIPTION:

    \b
    - USAGE:
        flow server query-all
    """
    client: FlowClient = ctx.obj["client"]
    response = client.service.query_all()
    prettify(response)


@server.command("query", short_help="Query Server Command")
@cli_args.SERVER_NAME
@click.pass_context
def query(ctx):
    """
    - DESCRIPTION:

    \b
    - USAGE:
        flow server query
    """
    client: FlowClient = ctx.obj["client"]
    response = client.service.query()
    prettify(response)


@server.command("registry", short_help="Registry Server Command")
@cli_args.SERVER_NAME_REQUIRED
@cli_args.HOST_REQUIRED
@cli_args.PORT_REQUIRED
@cli_args.PROTOCOL
@click.pass_context
def registry(ctx):
    """
    - DESCRIPTION:

    \b
    - USAGE:
        flow server registry --server-name xxx --host xxx --port xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.service.registry()
    prettify(response)


@server.command("delete", short_help="delete Server Command")
@cli_args.SERVER_NAME_REQUIRED
@click.pass_context
def delete(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow server registry --server-name xxx
    """
    config_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.service.delete(**config_data)
    prettify(response)


@server.command("query-service", short_help="query Service Command")
@cli_args.SERVER_NAME_REQUIRED
@cli_args.SERVICE_NAME_REQUIRED
@click.pass_context
def query_service(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow server query-service --server-name xxx --service-name xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.service.query_service(**kwargs)
    prettify(response)


@server.command("registry-service", short_help="Registry Service Command")
@cli_args.SERVER_NAME_REQUIRED
@cli_args.SERVICE_NAME_REQUIRED
@cli_args.URI_REQUIRED
@cli_args.METHOD
@cli_args.PARAMS
@cli_args.DATA
@cli_args.PROTOCOL
@click.pass_context
def registry_service(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow server registry-service --server-name xxx --service-name xxx --uri xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.service.registry_service(**kwargs)
    prettify(response)


@server.command("delete-service", short_help="Registry Service Command")
@cli_args.SERVER_NAME_REQUIRED
@cli_args.SERVICE_NAME_REQUIRED
@click.pass_context
def delete_service(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow server delete-service --server-name xxx --service-name xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.service.delete_service(**kwargs)
    prettify(response)
