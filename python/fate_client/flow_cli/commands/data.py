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
def data(ctx):
    """
    \b
    -description: Provides numbers of data operational commands, including upload, download, transformer and etc. For more details, please check out the help text.
    """
    pass


@data.command("upload")
@cli_args.CONF_PATH
@click.pass_context
def upload(ctx, **kwargs):
    """
    \b
    -description: Upload data to storage engine.

    \b
    -usage: flow data upload -c examples/upload/upload_guest.json
    """
    config_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.data.upload(**config_data)
    prettify(response)


@data.command("upload-file")
@cli_args.CONF_PATH
@click.pass_context
def upload_file(ctx, **kwargs):
    """
    \b
    -description: Upload file to storage engine.

    \b
    -usage: flow data upload-file -c examples/upload/upload_guest.csv
    """
    config_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.data.upload_file(**config_data)
    prettify(response)


@data.command("download-component")
@cli_args.NAME_REQUIRED
@cli_args.NAMESPACE_REQUIRED
@cli_args.PATH_REQUIRED
@click.pass_context
def download_component(ctx, **kwargs):
    """
    \b
    -description: Asynchronously downloading data through download component.

    \b
    -usage: flow data download-component --name 1bfaa4e6-4317-11ee-be20-16b977118319 --namespace upload -o /data/xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.data.download_component(**kwargs)
    prettify(response)


@data.command("transformer")
@cli_args.CONF_PATH
@click.pass_context
def dataframe_transformer(ctx, **kwargs):
    """
    \b
    -description: Converting Data Table to DataFrame.

    \b
    -usage: flow data transformer -c examples/transformer/transformer_guest.json
    """
    config_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.data.dataframe_transformer(**config_data)
    prettify(response)


@data.command("download")
@cli_args.NAME_REQUIRED
@cli_args.NAMESPACE_REQUIRED
@cli_args.PATH_REQUIRED
@click.pass_context
def download(ctx, **kwargs):
    """
    \b
    -description: Synchronous Data Download.

    \b
    -usage: flow data download --name 1bfaa4e6-4317-11ee-be20-16b977118319 --namespace upload -o /data/xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.data.download(**kwargs)
    prettify(response)
