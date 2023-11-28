import logging
import typing as t

from copy import copy

import httpx
import packaging.version
from httpx import URL

import deepchecks_llm_client
from deepchecks_llm_client.data_types import Tag, EnvType, AnnotationType, Step
from deepchecks_llm_client.utils import maybe_raise

__all__ = ['API']

logger = logging.getLogger(__name__)

TAPI = t.TypeVar('TAPI', bound='API')


class API:
    session: httpx.Client
    original_host: URL

    @classmethod
    def instantiate(cls: t.Type[TAPI], host: str, token: t.Optional[str] = None) -> TAPI:
        headers = {'Authorization': f'Basic {token}'} if token else None
        return cls(session=httpx.Client(base_url=host, headers=headers, timeout=60))

    def __init__(self, session: httpx.Client):
        self.session = copy(session)
        self.original_host = self.session.base_url
        self.session.base_url = self.session.base_url.join('/api/v1')
        self._app_name: str = None
        self._version_name: str = None
        self._env_type: EnvType = None
        self._tags: t.Dict[Tag, str] = {}

        try:
            backend_version = packaging.version.parse(self.retrieve_backend_version())
            client_version = packaging.version.parse(deepchecks_llm_client.__version__)
        except packaging.version.InvalidVersion as ex:
            raise Exception(f'Not able to compare backend and client versions, '
                            f'backend or client use incorrect or legacy versioning schema: {str(ex)}')
        else:
            if backend_version.major != client_version.major:
                raise Exception(
                    f'You are using an old, potentially incompatible with the current API, client version.\n'
                    f'Client version is {client_version}, Backend version is {backend_version}\n'
                    f'Upgrade "deepchecks-llm-client" version by running:\n'
                    f'>> pip install -U deepchecks-llm-client')

    def app_name(self, new_app_name: str):
        if new_app_name is None:
            raise ValueError("new_app_name cannot be set to None")
        self._app_name = new_app_name

    def get_app_name(self):
        return self._app_name

    def version_name(self, new_version_name: str):
        if new_version_name is None:
            raise ValueError("new_version_name cannot be set to None")
        self._version_name = new_version_name

    def get_version_name(self):
        return self._version_name

    def env_type(self, new_env_type: EnvType):
        if new_env_type is None:
            raise ValueError("new_env_type cannot be set to None")
        if new_env_type not in (EnvType.PROD, EnvType.EVAL):
            raise ValueError("new_env_type must be one of: EnvType.PROD or EnvType.EVAL")
        self._env_type = new_env_type

    def get_env_type(self):
        return self._env_type

    def set_tags(self, tags: t.Dict[Tag, str]):
        if tags is None:
            self._tags = {}
        else:
            self._tags = tags

    def retrieve_backend_version(self) -> str:
        payload = maybe_raise(self.session.get('backend-version')).json()
        return payload['version']

    def get_application(self, app_name: t.Union[str, None] = None) -> t.Dict[str, t.Any]:
        if app_name is None:
            app_name = self._app_name
        payload = maybe_raise(self.session.get('applications', params={"name": [app_name]})).json()

        return payload[0] if len(payload) > 0 else None

    def load_openai_data(self, data: t.List[t.Dict[str, t.Any]]) -> t.Optional[httpx.Response]:
        for row in data:
            row["user_data"] = self._tags
        return maybe_raise(self.session.post('openai-load', json=data,
                                             params={'app_name': self._app_name,
                                                     'version_name': self._version_name,
                                                     'env_type': self._env_type.value}))

    def annotate(self, ext_interaction_id: str, annotation: AnnotationType, reason: t.Optional[str] = None) -> t.Optional[httpx.Response]:
        return maybe_raise(self.session.post('annotations', json={"ext_interaction_id": ext_interaction_id,
                                                                  "value": annotation.value,
                                                                  "reason": reason}))

    def log_interaction(self,
                        input: str,
                        output: str,
                        full_prompt: str,
                        information_retrieval: str,
                        annotation: AnnotationType,
                        ext_interaction_id: str,
                        started_at: str,
                        finished_at: str,
                        steps: t.List[Step],
                        custom_props: t.Dict[str, t.Any],
                        annotation_reason: t.Optional[str] = None,
                        ) -> t.Optional[httpx.Response]:
        data = {"ext_interaction_id": ext_interaction_id,
                "input": input,
                "output": output,
                "full_prompt": full_prompt,
                "information_retrieval": information_retrieval,
                "app_name": self._app_name,
                "version_name": self._version_name,
                "env_type": self._env_type.value,
                "annotation": annotation.value if annotation else None,
                "annotation_reason": annotation_reason,
                "raw_json_data": {"user_data": self._tags},
                "steps": Step.as_jsonl(steps),
                "custom_props": custom_props}

        if started_at:
            data["started_at"] = started_at

        if finished_at:
            data["finished_at"] = finished_at

        return maybe_raise(self.session.post('interactions',
                                             json=data), expected=201)

    def get_interactions(self, application_version_id: int, limit: int, offset: int) -> t.List:
        return maybe_raise(
            self.session.post('get-interactions-by-filter',
                              json={
                                  "application_version_id": application_version_id,
                                  "environment": EnvType.EVAL.value,
                                  "limit": limit,
                                  "offset": offset
                              }, params={'return_topics': True, 'return_input_props': False})
        ).json()

    def get_interactions_csv(self, application_version_id: int, return_topics: bool,
                             return_output_props: bool, return_annotation_data: bool) -> str:
        return maybe_raise(
            self.session.post('interactions-download-all-by-filter',
                              json={
                                  "application_version_id": application_version_id,
                                  "environment": EnvType.EVAL.value,
                                  "limit": None,
                                  "offset": None,
                              }, params={'return_topics': return_topics,
                                         'return_output_props': return_output_props,
                                         'return_annotation_data': return_annotation_data})
        ).text

    def generate_topics(self):
        maybe_raise(self.session.post(f'generate-topics?env_type={self.get_env_type().value}'
                                      f'&app_name={self.get_app_name()}&app_version_name={self.get_version_name()}'))

    def update_application_config(self, application_id: int, file):
        if isinstance(file, str):
            file = open(file, "rb")
        data = {"file": ("filename", file)}
        maybe_raise(self.session.put(f'applications/{application_id}/config', files=data))

    def get_application_config(self, application_id: int, file_save_path: t.Union[str, None] = None) -> str:
        text = maybe_raise(self.session.get(f'applications/{application_id}/config')).text
        if file_save_path:
            with open(file_save_path, "w") as f:
                f.write(text)
        return text
