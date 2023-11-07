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


class PipelineCallBack(object):
    def on_fit_begin(self, *args, **kwargs):
        ...

    def on_fit_end(self, *args, **kwargs):
        ...

    def on_predict_begin(self, *args, **kwargs):
        ...

    def on_predict_end(self, *args, **kwargs):
        ...


class CallbackHandler(PipelineCallBack):
    def __init__(self):
        self._callbacks = []

    def add_callback(self, callback):
        self._callbacks.append(callback)

    def on_fit_begin(self, *args, **kwargs):
        return self.call_event("on_fit_begin", *args, **kwargs)

    def on_fit_end(self, *args, **kwargs):
        return self.call_event("on_fit_end", *args, **kwargs)

    def on_predict_begin(self, *args, **kwargs):
        return self.call_event("on_predict_begin", *args, **kwargs)

    def on_predict_end(self, *args, **kwargs):
        return self.call_event("on_prediction_end", *args, **kwargs)

    def call_event(self, func, *args, **kwargs):
        results = []
        for callback in self._callbacks:
            if hasattr(callback, func):
                result = getattr(callback, func)(
                    *args,
                    **kwargs
                )

                if result is not None:
                    results.append(result)

        return results


class JobInfoCallBack(PipelineCallBack):
    ENABLE_PIPELINE_JOB_INFO_CALLBACK =  "enable_pipeline_job_info_callback"
    PIPELINE_JOB_GLOBAL_SESSION_ID = "pipeline_job_info_global_session_id"
    PIPELINE_JOB_INFO = "pipeline_job_info"

    def __init__(self):
        super().__init__()

        self._enabled = False
        self._session_id = False
        self._callback_buf = []

        f = os.environ.get(self.ENABLE_PIPELINE_JOB_INFO_CALLBACK)
        if os.environ.get(self.ENABLE_PIPELINE_JOB_INFO_CALLBACK) == "1":
            self._enabled = True
            self._session_id = os.environ.get(self.PIPELINE_JOB_GLOBAL_SESSION_ID, None)

    def on_fit_begin(self, *args, **kwargs):
        self.call_event_begin(
            event="fit",
            status="submitted",
            **kwargs
        )

    def on_fit_end(self, *args, **kwargs):
        self.call_event_end(
            event="fit",
            status="finished",
            **kwargs
        )

    def on_predict_begin(self, *args, **kwargs):
        self.call_event_begin(
            event="predict",
            status="submitted",
            **kwargs
        )

    def on_predict_end(self, *args, **kwargs):
        self.call_event_end(
            event="predict",
            status="finished",
            **kwargs
        )

    def call_event_begin(self, event, status, **kwargs):
        if not self._enabled:
            return

        if "job_info" not in kwargs:
            raise ValueError("JobInfoCallBack is enabled, please provider job_info to use")

        job_info = kwargs["job_info"]

        if pre_job_info := os.environ.get(self.PIPELINE_JOB_INFO):
            self._callback_buf = json.loads(pre_job_info)

        self._callback_buf.append(
            dict(
                job_info=job_info,
                event=event,
                status=status,
                session_id=self._session_id
            )
        )

        os.environ[self.PIPELINE_JOB_INFO] = json.dumps(self._callback_buf)

    def call_event_end(self, event, status, **kwargs):
        if not self._enabled:
            return

        if "job_info" not in kwargs:
            raise ValueError("TaskInfoCallBack is enabled, please provider job_info to use")

        job_info = kwargs["job_info"]
        job_id = job_info["job_id"]

        for idx, callback_info in enumerate(self._callback_buf):
            if callback_info["job_info"]["job_id"] == job_id:
                self._callback_buf[idx] = (
                    dict(
                        job_info=job_info,
                        event=event,
                        status=status,
                        session_id=self._session_id
                    )
                )
                break

        os.environ[self.PIPELINE_JOB_INFO] = json.dumps(self._callback_buf)
