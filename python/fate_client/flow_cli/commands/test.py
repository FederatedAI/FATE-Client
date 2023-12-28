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
import os
import time
import click
from fate_client.flow_cli.utils import cli_args
from fate_client.flow_cli.utils.cli_utils import prettify
from fate_client.flow_sdk import FlowClient
from fate_client.pipeline import FateFlowPipeline
from fate_client.pipeline.components.fate import Evaluation, Reader
from fate_client.pipeline.components.fate import CoordinatedLR, PSI, HeteroSecureBoost


@click.group()
@click.pass_context
def test(ctx):
    """
    \b
    -description: fate test

    """
    pass


@test.command("toy")
@cli_args.GUEST_PARTYID_REQUIRED
@cli_args.HOST_PARTYID_REQUIRED
@cli_args.TIMEOUT
# @cli_args.TASK_CORES
@click.pass_context
def toy(ctx, **kwargs):
    """
    \b
    -description: Connectivity test.

    \b
    -usage: flow test toy -gid 9999 -hid 10000
    """
    flow_sdk = FlowClient(ip=ctx.obj["ip"], port=ctx.obj["http_port"], version=ctx.obj["api_version"],
                          app_id=ctx.obj.get("app_id"), app_token=ctx.obj.get("app_token"))
    submit_result = flow_sdk.test.toy(**kwargs)
    if submit_result["code"] == 0:
        job_id = submit_result["job_id"]
        for t in range(kwargs["timeout"]):
            party_id = kwargs["guest_party_id"]
            info = flow_sdk.site.info()
            if info.get("code") == 0:
                party_id = info.get("data", {}).get("party_id", kwargs["guest_party_id"])
            r = flow_sdk.job.query(job_id=job_id, party_id=party_id)
            if r["code"] == 0 and len(r["data"]):
                job_status = r["data"][0]["status"]
                print(f"toy test job {job_id} is {job_status}")
                if job_status in {"failed", "canceled"}:
                    warn_print(job_id)
                    break
                if job_status in {"success"}:
                    break
            time.sleep(1)
        else:
            print(f"timeout...")
            warn_print(job_id)
            try:
                flow_sdk.job.stop(job_id=job_id)
            except:
                pass
    else:
        prettify(submit_result)


def warn_print(job_id):
    print(f"You can use the command of 'flow job download-log -j {job_id} -o $download_dir' to download the logs.")


@test.command("min_test", short_help="Min Test Command")
@cli_args.GUEST_PARTYID_REQUIRED
@cli_args.HOST_PARTYID_REQUIRED
@cli_args.ARBITER_PARTYID_REQUIRED
@click.pass_context
def min_test(ctx, guest_party_id, host_party_id, arbiter_party_id, **kwargs):
    guest_party_id = int(guest_party_id)
    host_party_id = int(host_party_id)
    arbiter_party_id = int(arbiter_party_id)

    guest_train_data = {"table_name": "breast_hetero_guest", "namespace": "experiment"}
    host_train_data = {"table_name": "breast_hetero_host", "namespace": "experiment"}

    train_lr(guest_party_id, host_party_id, arbiter_party_id, guest_train_data, host_train_data)
    train_sbt(guest_party_id, host_party_id, arbiter_party_id, guest_train_data, host_train_data)


def train_lr(guest, host, arbiter, guest_train_data, host_train_data):
    # train lr
    pipeline = FateFlowPipeline().set_parties(guest=guest, host=host, arbiter=arbiter)

    reader_0 = Reader("reader_0")
    reader_0.guest.task_parameters(
        namespace=guest_train_data['namespace'],
        name=guest_train_data['table_name']
    )
    reader_0.hosts[0].task_parameters(
        namespace=host_train_data['namespace'],
        name=host_train_data['table_name'])

    psi_0 = PSI("psi_0", input_data=reader_0.outputs["output_data"])
    lr_0 = CoordinatedLR("lr_0",
                         optimizer={"method": "rmsprop", "optimizer_params": {"lr": 0.15},
                                    "alpha": 0.01},
                         learning_rate_scheduler={"method": "constant",
                                                  "scheduler_params": {"factor": 0.5, "total_iters": 5}},
                         epochs=5,
                         batch_size=None,
                         init_param={"fit_intercept": True, "method": "random_uniform", "random_state": 42},
                         train_data=psi_0.outputs["output_data"],
                         early_stop="diff", )

    evaluation_0 = Evaluation("evaluation_0",
                              runtime_parties=dict(guest=guest),
                              default_eval_setting="binary",
                              input_data=lr_0.outputs["train_output_data"])

    pipeline.add_tasks([reader_0, psi_0, lr_0, evaluation_0])

    pipeline.compile()
    pipeline.fit()

    # get auc
    # todo get_task_info("lr_0")
    metric_summary = pipeline.get_task_info("evaluation_0").get_output_metric()[0]["data"]
    auc = get_auc(metric_summary, "lr_0")

    # predict
    pipeline.deploy([psi_0, lr_0])

    predict_pipeline = FateFlowPipeline()

    reader_1 = Reader("reader_1")
    reader_1.guest.task_parameters(
        namespace=guest_train_data['namespace'],
        name=guest_train_data['table_name']
    )
    reader_1.hosts[0].task_parameters(
        namespace=host_train_data['namespace'],
        name=host_train_data['table_name']
    )

    deployed_pipeline = pipeline.get_deployed_pipeline()
    deployed_pipeline.psi_0.input_data = reader_1.outputs["output_data"]

    predict_pipeline.add_tasks([reader_1, deployed_pipeline])
    predict_pipeline.compile()
    predict_pipeline.predict()
    return


def train_sbt(guest, host, arbiter, guest_train_data, host_train_data):
    # train sbt
    pipeline = FateFlowPipeline().set_parties(guest=guest, host=host, arbiter=arbiter)

    reader_0 = Reader("reader_0",runtime_parties=dict(guest=guest, host=host))
    reader_0.guest.task_parameters(
        namespace=guest_train_data['namespace'],
        name=guest_train_data['table_name']
    )

    reader_0.hosts[0].task_parameters(
        namespace=host_train_data['namespace'],
        name=host_train_data['table_name']
    )
    psi_0 = PSI("psi_0", input_data=reader_0.outputs["output_data"])
    sbt_0 = HeteroSecureBoost("sbt_0",
                              num_trees=2,
                              max_depth=2,
                              min_leaf_node=2,
                              goss=False,
                              he_param={"kind": "ou", "key_length": 1024},
                              train_data=psi_0.outputs["output_data"])

    evaluation_0 = Evaluation("evaluation_0",
                              runtime_parties=dict(guest=guest),
                              label_column_name='label',
                              default_eval_setting="binary",
                              input_data=sbt_0.outputs["train_data_output"])

    pipeline.add_tasks([reader_0, psi_0, sbt_0, evaluation_0])
    pipeline.compile()
    pipeline.fit()
    pipeline.deploy([psi_0, sbt_0])

    predict_pipeline = FateFlowPipeline()

    reader_1 = Reader("reader_1", runtime_parties=dict(guest=guest, host=host))
    reader_1.guest.task_parameters(
        namespace=guest_train_data['namespace'],
        name=guest_train_data['table_name']
    )

    reader_1.hosts[0].task_parameters(
        namespace=host_train_data['namespace'],
        name=host_train_data['table_name']
    )

    deployed_pipeline = pipeline.get_deployed_pipeline()
    deployed_pipeline.psi_0.input_data = reader_1.outputs["output_data"]
    predict_pipeline.add_tasks([reader_1, deployed_pipeline])
    predict_pipeline.compile()
    predict_pipeline.predict()


def get_auc(metric_summary, model_name):
    metric_group = metric_summary.get(model_name).get('train_set')
    for metric_pair in metric_group:
        if metric_pair.get('metric') == 'auc':
            return metric_pair.get('val')

