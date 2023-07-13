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


@click.group(short_help="Model Operations")
@click.pass_context
def model(ctx):
    """
    \b
    Provides numbers of data operational commands, including upload, download and etc.
    For more details, please check out the help text.
    """
    pass


@model.command("deploy", short_help="Deploy model")
@click.option("--cpn-list", type=click.STRING,
              help="User inputs a string to specify component list")
@click.option("--cpn-path", type=click.Path(exists=True),
              help="User specifies a file path which records the component list.")
@click.option("--dsl-path", type=click.Path(exists=True),
              help="User specified predict dsl file")
@click.option("--cpn-step-index", type=click.STRING, multiple=True,
              help="Specify a checkpoint model to replace the pipeline model. "
                   "Use : to separate component name and step index (E.g. --cpn-step-index cpn_a:123)")
@click.option("--cpn-step-name", type=click.STRING, multiple=True,
              help="Specify a checkpoint model to replace the pipeline model. "
                   "Use : to separate component name and step name (E.g. --cpn-step-name cpn_b:foobar)")
@click.pass_context
def deploy(ctx, **kwargs):
    """
    - DESCRIPTION:
        Deploy model.

    \b
    - USAGE:
        flow model deploy --model-id $MODEL_ID --model-version $MODEL_VERSION
    """
    client: FlowClient = ctx.obj["client"]
    response = client.model.deploy(**kwargs)
    prettify(response)


@model.command("load", short_help="Load Model Command")
@cli_args.JOBID
@click.option("-c", "--conf-path", type=click.Path(exists=True),
              help="Configuration file path.")
@click.pass_context
def load(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
        Download Data Table.

    \b
    - USAGE:
        flow data download -c fateflow/examples/download/download_table.json
    """
    client: FlowClient = ctx.obj["model"]
    response = client.model.load(**kwargs)
    prettify(response)


@model.command("migrate", short_help="Migrate Model Command")
@cli_args.CONF_PATH
@click.pass_context
def migrate(ctx, **kwargs):
    """
    \b
    - DESCRIPTION:
        Migrate Model Command.

    \b
    - USAGE:
        flow model migrate -c fate_flow/examples/migrate_model.json
    """
    client: FlowClient = ctx.obj["client"]
    response = client.model.migrate(**kwargs)
    prettify(response)


@model.command("export", short_help="Export Model Command")
@cli_args.CONF_PATH
@click.pass_context
def export_model(ctx, **kwargs):
    """
    \b
    - DESCRIPTION:
        Export the model to a file or storage engine.

    \b
    - USAGE:
        flow model export -c fate_flow/examples/export_model.json
        # flow model export -c fate_flow/examples/store_model.json --to-database
    """
    config_data, dsl_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.model.export(**config_data)
    prettify(response)


@model.command("store", short_help="Migrate Model Command")
@cli_args.CONF_PATH
@click.option('--from-database', is_flag=True, default=False,
              help="If specified and there is a valid database environment, fate flow will import model from database "
                   "which you specified in configuration file.")
@click.pass_context
def store(ctx, **kwargs):
    """
    \b
    - DESCRIPTION:
        Export the model to a file or storage engine.

    \b
    - USAGE:
        flow model export -c fate_flow/examples/export_model.json
        flow model export -c fate_flow/examples/store_model.json --to-database
    """
    client: FlowClient = ctx.obj["client"]
    response = client.model.store(**kwargs)
    prettify(response)


@model.command("restore", short_help="Migrate Model Command")
@cli_args.CONF_PATH
@click.option('--from-database', is_flag=True, default=False,
              help="If specified and there is a valid database environment, fate flow will import model from database "
                   "which you specified in configuration file.")
@click.pass_context
def restore(ctx, **kwargs):
    """
    \b
    - DESCRIPTION:
        Export the model to a file or storage engine.

    \b
    - USAGE:
        flow model export -c fate_flow/examples/export_model.json
        flow model export -c fate_flow/examples/store_model.json --to-database
    """
    client: FlowClient = ctx.obj["client"]
    response = client.model.restore(**kwargs)
    prettify(response)
