import functools
import logging
import time
from datetime import datetime

import openai
from deepchecks_llm_client.api import API
from deepchecks_llm_client.utils import handle_exceptions, set_verbosity

logging.basicConfig()
logger = logging.getLogger(__name__)


class OpenAIInstrumentor:

    def __init__(self, api: API, verbose: bool = False, log_level: int = logging.WARNING, auto_collect: bool = False):
        self.api = api
        self._auto_collect = auto_collect
        logger.setLevel(log_level)
        set_verbosity(verbose, logger)

        self.openai_version = "0.0.0"
        try:
            from importlib import metadata
            self.openai_version = metadata.version('openai')
        except Exception as ex:
            pass

    @staticmethod
    def _patched_call(original_fn, patched_fn):
        @functools.wraps(original_fn)
        def _inner_patch(*args, **kwargs):
            return patched_fn(original_fn, *args, **kwargs)

        return _inner_patch

    def auto_collect(self, auto_collect: bool):
        self._auto_collect = auto_collect
        return self

    def patcher_create(self, original_fn, *args, **kwargs):
        if self._auto_collect:
            self._before_run_log_print(args, kwargs, original_fn)

            started_at = datetime.utcnow()
            result = original_fn(*args, **kwargs)
            finished_at = datetime.utcnow()

            self._after_run_actions(args, kwargs, original_fn, result, started_at, finished_at)
        else:
            logger.debug(f"auto collect is off, skipping logging {original_fn.__qualname__} to Deepchecks")
            result = original_fn(*args, **kwargs)
        return result

    async def patcher_acreate(self, original_fn, *args, **kwargs):
        if self._auto_collect:
            self._before_run_log_print(args, kwargs, original_fn)

            started_at = datetime.utcnow()
            result = await original_fn(*args, **kwargs)
            finished_at = datetime.utcnow()

            self._after_run_actions(args, kwargs, original_fn, result, started_at, finished_at)
        else:
            logger.debug(f"auto collect is off, skipping logging {original_fn.__qualname__} to Deepchecks")
            result = await original_fn(*args, **kwargs)
        return result

    @handle_exceptions(logger)
    def _after_run_actions(self, args, kwargs, original_fn, result, started_at, finished_at):
        time_delta = (finished_at - started_at).total_seconds() * 1000
        logger.info("Finished running function: %s, time delta: %sms", original_fn.__qualname__, time_delta)
        logger.debug("Function Output: %s", result)

        # Obfuscate the api-key
        if kwargs.get("api_key"):
            kwargs["api_key"] = f"last-4-digits-{kwargs['api_key'][-4:]}"

        event_dict = {
            "request": {"func_name": original_fn.__qualname__, "args": args, "kwargs": kwargs},
            "output": result.to_dict_recursive(),
            "runtime_data": {"response_time": time_delta,
                             "openai_version": self.openai_version,
                             'started_at': started_at.isoformat(),
                             'finished_at': finished_at.isoformat()},
        }
        self.api.load_openai_data(data=[event_dict])

        logger.debug("Reported this event to deepchecks server:\n%s", event_dict)

    @staticmethod
    def _before_run_log_print(args, kwargs, original_fn):
        logger.info("Running the original function: %s. args: %s, kwargs: %s", original_fn.__qualname__, args, kwargs)

    def perform_patch(self):
        try:
            openai.ChatCompletion.acreate = self._patched_call(
                openai.ChatCompletion.acreate, self.patcher_acreate
            )
        except AttributeError:
            pass

        try:
            openai.ChatCompletion.create = self._patched_call(
                openai.ChatCompletion.create, self.patcher_create
            )
        except AttributeError:
            pass

        try:
            openai.Completion.acreate = self._patched_call(
                openai.Completion.acreate, self.patcher_acreate
            )
        except AttributeError:
            pass

        try:
            openai.Completion.create = self._patched_call(
                openai.Completion.create, self.patcher_create
            )
        except AttributeError:
            pass
