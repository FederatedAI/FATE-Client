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
from ..utils.cli_utils import load_yaml, preprocess,prettify
from fate_client.flow_sdk import FlowClient


@click.group()
@click.pass_context
def model(ctx):
    """
    \b
    -description: Model Operations
    """
    pass


@model.command("export")
@cli_args.MODEL_ID_REQUIRED
@cli_args.MODEL_VERSION_REQUIRED
@cli_args.PARTYID_REQUIRED
@cli_args.ROLE_IDE_REQUIRED
@cli_args.PATH_REQUIRED
@click.pass_context
def export_model(ctx, **kwargs):
    """
    \b
    -description: Export the model to a file.

    \b
    -usage: flow model export --model-id xxx --model-version xxx -p 9999 -r guest -o ./model/
    """
    client: FlowClient = ctx.obj["client"]
    response = client.model.export(**kwargs)
    prettify(response)


@model.command("import")
@cli_args.MODEL_ID_REQUIRED
@cli_args.MODEL_VERSION_REQUIRED
@cli_args.INPUT_PATH_REQUIRED
@click.pass_context
def import_model(ctx, **kwargs):
    """
    \b
    -description: Import the model to storage engine.

    \b
    -usage: flow model import --model-id xxx --model-version xxx -i $input_path
    """
    # config_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.model.import_model(**kwargs)
    prettify(response)


@model.command("delete")
@cli_args.MODEL_ID_REQUIRED
@cli_args.MODEL_VERSION_REQUIRED
@cli_args.ROLE_IDE
@cli_args.PARTYID
@cli_args.TASK_NAME
@cli_args.OUTPUT_KEY
@click.pass_context
def delete_model(ctx, **kwargs):
    """
    \b
    -description: Delete Models Based on Conditions

    \b
    -usage: flow model delete --model-id xxx  --model-version xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.model.delete_model(**kwargs)
    prettify(response)
