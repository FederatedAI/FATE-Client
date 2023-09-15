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

from pathlib import Path
from ruamel import yaml


__all__ = ["StatusCode", "FlowConfig", "SiteInfo"]


with Path(__file__).parent.parent.parent.joinpath("settings.yaml").resolve().open("r") as fin:
    __DEFAULT_CONFIG: dict = yaml.safe_load(fin)


def get_default_config():
    return __DEFAULT_CONFIG


CONSOLE_DISPLAY_LOG = get_default_config().get("console_display_log", True)
if CONSOLE_DISPLAY_LOG is None:
    CONSOLE_DISPLAY_LOG = True


class StatusCode(object):
    SUCCESS = 0
    FAIL = 1
    CANCELED = 2


class SiteInfo(object):
    conf = get_default_config().get("pipeline", {}).get("site_info", {})
    ROLE = conf.get("local_role")
    PARTY_ID = conf.get("local_party_id")


class FlowConfig(object):
    conf = get_default_config().get("flow_service", {})
    IP = conf.get("ip")
    PORT = conf.get("port")
    VERSION = conf.get("api_version")


class LOGGER(object):
    def __init__(self, conf):
        self._level = conf.get("logger", {}).get("level", "DEBUG")
        self._debug_mode = conf.get("logger", {}).get("debug_mode", True)

    @property
    def level(self):
        return self._level

    @property
    def debug_mode(self):
        return self._debug_mode
