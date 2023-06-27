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


@click.group(short_help="Job Operations")
@click.pass_context
def job(ctx):
    """
    \b
    Provides numbers of job operational commands, including submit, stop, query and etc.
    For more details, please check out the help text.
    """
    pass


@job.command("submit", short_help="Submit Job Command")
@cli_args.CONF_PATH
@click.pass_context
def submit(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    Submit a pipeline job.
    Used to be 'submit_job'.

    \b
    - USAGE:
        flow job submit -c fate_flow/examples/lr/standalone/lr_train_dag.yaml
    """
    print(f'submit:{kwargs}')
    dag_schema = load_yaml(kwargs.get("conf_path"))
    client: FlowClient = ctx.obj["client"]
    #response = client.job.submit({"dag_schema":dag_schema})
    response = client.job.submit(dag_schema=dag_schema)
    prettify(response)

@job.command("query", short_help="query Job Command")
@cli_args.JOBID
@cli_args.ROLE
@cli_args.PARTYID
@cli_args.STATUS
@click.pass_context
def query(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    Query job information by filters.
    Used to be 'query_job'.

    \b
    - USAGE:
        flow job query -j $JOB_ID -r guest -p 9999 -s success
    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.query(**kwargs)
    prettify(response)


@job.command("stop", short_help="stop Job Command")
@cli_args.JOBID_REQUIRED
@click.pass_context
def stop(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
        Stop a specified job.

    \b
    - USAGE:
       flow job stop -j $JOB_ID
    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.stop(**kwargs)
    prettify(response)


@job.command("rerun", short_help="rerun Job Command")
@cli_args.JOBID_REQUIRED
@click.pass_context
def rerun(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
        rerun a job when it was failed.

    \b
    - USAGE:
       flow job stop -j $JOB_ID
    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.rerun(**kwargs)
    prettify(response)


@job.command("list", short_help="stop Job Command")
@cli_args.LIMIT
@click.pass_context
def job_list(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
        get List job.
    \b
    - USAGE:
        flow job list
        flow job list -l 30
    """
    # config_data, dsl_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.job.query_job_list(**kwargs)
    prettify(response)


@job.command("log", short_help="Log Job Command")
@cli_args.JOBID_REQUIRED
@cli_args.OUTPUT_PATH_REQUIRED
@click.pass_context
def log(ctx, **kwargs):
    """
    - DESCRIPTION:
        Download Log Files of A Specified Job.

    \b
    - USAGE:
        flow job log -j JOB_ID --output-path ./examples/
    """
    # config_data, dsl_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.job.download_log(**kwargs)
    prettify(response)


@job.command("clean", short_help="Clean Job Command")
@cli_args.JOBID
@click.pass_context
def clean(ctx, **kwargs):
    """
    - DESCRIPTION:
        Clean processor, data table and metric data.
        Used to be 'clean_job'.

    \b
    - USAGE:
        flow job clean -j $JOB_ID
    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.job_clean(**kwargs)
    prettify(response)


@job.command("dependency", short_help="Clean Job Command")
@cli_args.JOBID
@cli_args.ROLE
@cli_args.PARTYID
@click.pass_context
def dependency(ctx, **kwargs):
    """
    - DESCRIPTION:

    \b
    - USAGE:

    """
    client: FlowClient = ctx.obj["client"]
    response = client.job.dag_dependency(**kwargs)
    prettify(response)
