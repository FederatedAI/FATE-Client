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
# import sys
# sys.path.append(r'D:\projects\FATE-Client\python')

import click
from ruamel import yaml

from fate_client.flow_sdk import FlowClient
from fate_client.flow_cli.commands import job, data, log, model, output, permission, provider, service, site, table, task, queue
from fate_client.flow_cli.utils.cli_utils import prettify


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(short_help='Fate Flow Client', context_settings=CONTEXT_SETTINGS)
@click.pass_context
def flow_cli(ctx):
    '''
    Fate Flow Client
    '''
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand == 'init':
        return

    with open(os.path.join(os.path.dirname(__file__), 'settings.yaml'), 'r') as fin:
        config = yaml.safe_load(fin)
    if not config.get('api_version'):
        raise ValueError('api_version in config is required')
    ctx.obj['api_version'] = config['api_version']

    if config.get('ip') and config.get('port'):
        ctx.obj['ip'] = config['ip']
        ctx.obj['http_port'] = int(config['port'])
        ctx.obj['server_url'] = f'http://{ctx.obj["ip"]}:{ctx.obj["http_port"]}/{config["api_version"]}'
        if config.get('app_id') and config.get('app_token'):
            ctx.obj['app_id'] = config['app_id']
            ctx.obj['app_token'] = config['app_token']
    else:
        raise ValueError('Invalid configuration file. Did you run "flow init"?')

    ctx.obj['initialized'] = (config.get('ip') and config.get('port'))
    if ctx.obj['initialized']:
        ctx.obj["client"] = FlowClient(
            ip=config.get('ip'), port=config.get('port'), version=config.get("api_version"),
            app_id=config.get("app_id"), app_token=config.get('app_token')
        )


@flow_cli.command('init', short_help='Flow CLI Init Command')
@click.option('--ip', type=click.STRING, help='Fate flow server ip address.')
@click.option('--port', type=click.INT, help='Fate flow server port.')
@click.option('--app-id', type=click.STRING, help='APP key for sign requests.')
@click.option('--app-token', type=click.STRING, help='Secret key for sign requests.')
@click.option('--reset', is_flag=True, default=False,
              help='If specified, initialization settings would be reset to none. Users should init flow again.')
def initialization(**kwargs):
    """
    - DESCRIPTION:
        Flow CLI Init Command. provide ip and port of a valid fate flow server.
        If the server enables client authentication, you need to configure app-id and app-token


    - USAGE:
        flow init --ip 127.0.0.1 --port 9380
        flow init --app-id xxx --app-token

    """

    with open(os.path.join(os.path.dirname(__file__), 'settings.yaml'), 'r') as fin:
        config = yaml.safe_load(fin)

    if kwargs.get('reset'):
        config['api_version'] = 'v2'
        for i in ('ip', 'port', 'app_id', 'app_token'):
            config[i] = None

        with open(os.path.join(os.path.dirname(__file__), 'settings.yaml'), 'w') as fout:
            yaml.dump(config, fout, Dumper=yaml.RoundTripDumper)
        prettify(
            {
                'retcode': 0,
                'retmsg': 'Fate Flow CLI has been reset successfully. '
                          'Please do initialization again before you using flow CLI v2.'
            }
        )
    else:
        config['api_version'] = 'v2'
        _update = False
        for i in ('ip', 'port', 'app_id', 'secret_token'):
            if kwargs.get(i):
                config[i] = kwargs[i]
                _update = True

        if _update:
            with open(os.path.join(os.path.dirname(__file__), 'settings.yaml'), 'w') as fout:
                yaml.dump(config, fout, Dumper=yaml.RoundTripDumper)
            prettify(
                {
                    'retcode': 0,
                    'retmsg': 'Fate Flow CLI has been initialized successfully.'
                }
            )
        else:
            prettify(
                {
                    'retcode': 100,
                    'retmsg': 'Fate Flow CLI initialization failed.'
                }
            )


flow_cli.add_command(job.job)
flow_cli.add_command(data.data)
flow_cli.add_command(log.log)
flow_cli.add_command(model.model)
flow_cli.add_command(output.output)
flow_cli.add_command(permission.permission)
flow_cli.add_command(provider.provider)
flow_cli.add_command(queue.queue)
flow_cli.add_command(service.service)
flow_cli.add_command(site.site)
flow_cli.add_command(table.table)
flow_cli.add_command(task.task)


if __name__ == '__main__':
    print(f'--start--')
    flow_cli()
