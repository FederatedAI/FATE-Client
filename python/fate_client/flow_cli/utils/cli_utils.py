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

import json
import os
import click
import requests
from ruamel import yaml
from functools import wraps


def prettify(response):
    # format json
    if isinstance(response, requests.models.Response):
        try:
            response = response.json()
        except json.decoder.JSONDecodeError:
            response = {
                'retcode': 100,
                'retmsg': response.text,
            }

    click.echo(json.dumps(response, indent=4, ensure_ascii=False))
    click.echo('')

    return response


def check_abs_path(path):
    if os.path.isabs(path):
        return path
    return os.path.abspath(os.path.join(os.getcwd(), path))


def load_yaml(path):
    with open(path, "r") as fr:
        return yaml.safe_load(fr)


def ctx_wraps(func):
    @wraps(func)
    def _wrapper(ctx, *args, **kwargs):
        kwargs["client"] = ctx.obj["client"]
        return func(*args, **kwargs)
    return _wrapper


def preprocess(**kwargs):
    config_data = {}

    if kwargs.get('conf_path'):
        conf_path = os.path.abspath(kwargs.get('conf_path'))
        with open(conf_path, 'r') as conf_fp:
            config_data = json.load(conf_fp)

        if config_data.get('output_path'):
            config_data['output_path'] = os.path.abspath(config_data['output_path'])

        if ('party_id' in kwargs.keys()) or ('role' in kwargs.keys()):
            config_data['local'] = config_data.get('local', {})
            if kwargs.get('party_id'):
                config_data['local']['party_id'] = kwargs.get('party_id')
            if kwargs.get('role'):
                config_data['local']['role'] = kwargs.get('role')
    config_data.update(dict((k, v) for k, v in kwargs.items() if v is not None))

    dsl_data = {}
    if kwargs.get('dsl_path'):
        dsl_path = os.path.abspath(kwargs.get('dsl_path'))
        with open(dsl_path, 'r') as dsl_fp:
            dsl_data = json.load(dsl_fp)
    return config_data, dsl_data


