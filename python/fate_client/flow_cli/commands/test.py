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
import time
import click
from fate_client.flow_cli.utils import cli_args
from fate_client.flow_cli.utils.cli_utils import prettify
from fate_client.flow_sdk import FlowClient


@click.group(short_help="FATE Flow Test Operations")
@click.pass_context
def test(ctx):
    """
    \b
    Provides numbers of component operational commands, including metrics, parameters and etc.
    For more details, please check out the help text.
    """
    pass


@test.command("toy", short_help="Toy Test Command")
@cli_args.GUEST_PARTYID_REQUIRED
@cli_args.HOST_PARTYID_REQUIRED
@cli_args.TIMEOUT
@cli_args.TASK_CORES
@click.pass_context
def toy(ctx, **kwargs):
    flow_sdk = FlowClient(ip=ctx.obj["ip"], port=ctx.obj["http_port"], version=ctx.obj["api_version"],
                          app_id=ctx.obj.get("app_id"), app_token=ctx.obj.get("app_token"))
    submit_result = flow_sdk.test.toy(**kwargs)
    if submit_result["code"] == 0:
        job_id = submit_result["job_id"]
        for t in range(kwargs["timeout"]):
            r = flow_sdk.job.query(job_id=job_id, role="guest", party_id=kwargs["guest_party_id"])
            if r["code"] == 0 and len(r["data"]):
                job_status = r["data"][0]["status"]
                print(f"toy test job {job_id} is {job_status}")
                if job_status in {"success", "failed", "canceled"}:
                    check_log(flow_sdk, kwargs["guest_party_id"], job_id, job_status)
                    break
            time.sleep(1)
        else:
            print(f"check job status timeout")
            check_log(flow_sdk, kwargs["guest_party_id"], job_id, job_status)
    else:
        prettify(submit_result)


def check_log(flow_sdk, party_id, job_id, job_status):
    _path = "../..fate_flow/logs/toy"
    r = flow_sdk.job.download_log(job_id=job_id, path=_path)
    if r["code"] == 0:
        log_msg = flow_sdk.test.check_toy(party_id, job_status, _path)
        try:
            for msg in log_msg:
                print(msg)
        except BaseException:
            print(f"auto check log failed, please check {_path}")
    else:
        print(f"get log failed, please check PROJECT_BASE/logs/{job_id} on the fateflow server machine")