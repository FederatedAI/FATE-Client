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


@click.group(short_help="Data Operations")
@click.pass_context
def data(ctx):
    """
    \b
    Provides numbers of data operational commands, including upload, download and etc.
    For more details, please check out the help text.
    """
    pass


@data.command("upload", short_help="Upload Table Command")
@cli_args.CONF_PATH
#@click.option('--verbose', is_flag=True, default=False,
#              help="If specified, verbose mode will be turn on. "
#                   "Users can have feedback on upload task in progress. (default: False)")
#@click.option('--drop', is_flag=True, default=False,
#              help="If specified, data of old version would be replaced by the current version. "
#                   "Otherwise, current upload task would be rejected. (default: False)")
@click.pass_context
def upload(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
        Upload Data Table.

    \b
    - USAGE:
        flow data upload -c fateflow/examples/upload/upload_guest.json
        flow data upload -c fateflow/examples/upload/upload_host.json --verbose --drop
    """
    config_data, dsl_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    if "conf_path" in config_data.keys():config_data.pop("conf_path")
    response = client.data.upload(**config_data)
    prettify(response)


@data.command("download", short_help="Download Table Command")
# @cli_args.TABLE_NAME
# @cli_args.NAMESPACE
@cli_args.CONF_PATH
@click.pass_context
def download(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
        Download Data Table.

    \b
    - USAGE:
        flow data download -c fateflow/examples/download/download_table.json
    """
    config_data, dsl_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    # if "conf_path" in config_data.keys():config_data.pop("conf_path")
    response = client.data.download(**config_data)
    prettify(response)


@data.command("transformer", short_help="dataframe transformer")
@cli_args.CONF_PATH
@click.pass_context
def dataframe_transformer(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
        Download Data Table.

    \b
    - USAGE:
        flow data download -c fateflow/examples/download/download_table.json
    """
    config_data, dsl_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    if "conf_path" in config_data.keys():config_data.pop("conf_path")
    response = client.data.dataframe_transformer(**config_data)
    prettify(response)
