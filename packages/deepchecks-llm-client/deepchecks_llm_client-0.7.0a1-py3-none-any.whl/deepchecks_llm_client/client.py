import logging
import typing as t
import uuid
from datetime import datetime
from io import StringIO

import pandas as pd

from deepchecks_llm_client.api import API
from deepchecks_llm_client.data_types import Tag, EnvType, AnnotationType, GoldenSetInteraction, Step
from deepchecks_llm_client.openai_instrumentor import OpenAIInstrumentor
from deepchecks_llm_client.utils import handle_exceptions, set_verbosity

__all__ = ["dc_client", "DeepchecksLLMClient"]

logging.basicConfig()
logger = logging.getLogger(__name__)
init_logger = logging.Logger(__name__ + ".init")

DEFAULT_VERSION_NAME = '0.0.1'
DEFAULT_ENV_TYPE = EnvType.PROD


class DeepchecksLLMClientError(Exception):
    pass


class DeepchecksLLMClient:
    def __init__(self):
        self._api: API = None
        self.app: t.Dict[str, t.Any] = None
        self.instrumentor: OpenAIInstrumentor = None
        self._initialized: bool = False
        self._verbose: bool = False
        self._log_level: int = logging.WARNING

    @handle_exceptions(init_logger)
    def init(self,
             host: str,
             api_token: str,
             app_name: str,
             version_name: str = DEFAULT_VERSION_NAME,
             env_type: EnvType = DEFAULT_ENV_TYPE,
             auto_collect: bool = True,
             init_verbose: bool = True,
             verbose: bool = False,
             log_level: int = logging.WARNING
             ):
        """
        Connect to Deepchecks LLM Server

        Parameters
        ==========
        host : str
            Deepchecks host to communicate with
        api_token : str
            Deepchecks API Token (can be generated from the UI)
        app_name : str
            Application name to connect to
        version_name : str, default='0.0.1'
            Version name to connect to inside the application,
            if Version name does not exist SDK will create it automatically,
        env_type : EnvType, default=EnvType.PROD
            could be EnvType.PROD (for 'Production') or EnvType.EVAL (for 'Evaluation')
        auto_collect : bool, default=True
            Auto collect calls to LLM Models
        init_verbose: bool, default=True
            Write log messages during the init phase and non-prod phases such as golden_set()
        verbose : bool, default=False
            Write log messages (by default we are in silence mode)
        log_level: int, default=logging.WARNING
            In case that verbose or init_verbose is True,
            this parameter will set SDK loggers logging level

        Returns
        =======
        None
        """
        if self._initialized:
            logger.warning(
                "Deepchecks client was initialized already. "
                "We will ignore newly provided parameters"
            )
            return

        logger.setLevel(log_level)
        self._log_level = log_level
        set_verbosity(init_verbose, init_logger)
        set_verbosity(verbose, logger)
        self._verbose = verbose

        if self._api is None:
            if host is not None and api_token is not None:
                self._api = API.instantiate(host=host, token=api_token)
            else:
                raise DeepchecksLLMClientError('host/token parameters must be provided')


        if app_name is None:
            raise DeepchecksLLMClientError('app_name must be supplied')
        self.app = self._api.get_application(app_name)
        if not self.app:
            raise DeepchecksLLMClientError(f'Application: "{app_name}", does not exist, please create it via the UI')

        self.app_name(app_name).version_name(version_name).env_type(env_type)

        self.instrumentor = None
        if auto_collect:
            self.instrumentor = OpenAIInstrumentor(self.api, verbose, log_level, auto_collect)
            self.instrumentor.perform_patch()
        self._initialized = True

    @property
    def initialized(self):
        return self._initialized

    @property
    @handle_exceptions(logger)
    def api(self) -> API:
        if self._api:
            return self._api
        raise DeepchecksLLMClientError("dc_client was not initialized correctly, please re-create it")

    @handle_exceptions(logger, return_self=True)
    def app_name(self, new_app_name: str):
        self.api.app_name(new_app_name)
        return self

    @handle_exceptions(logger, return_self=True)
    def version_name(self, new_version_name: str):
        self.api.version_name(new_version_name)
        return self

    @handle_exceptions(logger, return_self=True)
    def env_type(self, new_env_type: EnvType):
        self.api.env_type(new_env_type)
        return self

    @handle_exceptions(logger)
    def auto_collect(self, enabled: bool):
        if not self.instrumentor:
            self.instrumentor = OpenAIInstrumentor(
                api=self.api, verbose=self._verbose, log_level=self._log_level, auto_collect=enabled,
            )
            self.instrumentor.perform_patch()
        else:
            self.instrumentor.auto_collect(auto_collect=enabled)
        return self

    @handle_exceptions(logger)
    def set_tags(self, tags: t.Dict[Tag, str]):
        self.api.set_tags(tags)
        return self

    @handle_exceptions(logger)
    def annotate(self, ext_interaction_id: str, annotation: AnnotationType, reason: t.Optional[str] = None):
        self.api.annotate(ext_interaction_id, annotation, reason=reason)
        return self

    @handle_exceptions(logger)
    def log_interaction(self,
                        input: str,
                        output: str,
                        full_prompt: str = None,
                        information_retrieval: str = None,
                        annotation: AnnotationType = None,
                        annotation_reason: str = None,
                        ext_interaction_id: str = None,
                        started_at: t.Union[datetime, None] = None,
                        finished_at: t.Union[datetime, None] = None,
                        steps: t.List[Step] = None,
                        custom_props: t.Dict[str, t.Any] = None) -> t.Union[str, uuid.UUID, None]:
        result = self.api.log_interaction(input=input,
                                          output=output,
                                          full_prompt=full_prompt,
                                          information_retrieval=information_retrieval,
                                          annotation=annotation,
                                          annotation_reason=annotation_reason,
                                          ext_interaction_id=ext_interaction_id,
                                          started_at=started_at.isoformat() if started_at else None,
                                          finished_at=finished_at.isoformat() if finished_at else None,
                                          steps=steps,
                                          custom_props=custom_props)
        return result.json()

    @handle_exceptions(logger)
    def update_application_config(self, file):
        self.api.update_application_config(application_id=self.app['id'], file=file)

    @handle_exceptions(logger)
    def get_application_config(self, file_save_path: t.Union[str, None] = None) -> str:
        return self.api.get_application_config(application_id=self.app['id'], file_save_path=file_save_path)

    @handle_exceptions(init_logger)
    def golden_set_iterator(self, version_name: t.Union[str, None] = None) -> t.Iterable[GoldenSetInteraction]:
        """
        Fetch all interactions from the golden set (EnvType.EVAL), as iterable
        Supports pagination, so this API is suitable for iterating large amount of data

        Parameters
        ----------
        version_name : str
            version name to fetch interactions from, if no version name was supplied
            the latest created version in the application will be used (mostly useful
            when integrating the golden set and rerun it in the CI)

        Returns
        -------
        Iterable collection of interactions

        """
        golden_set_version = self._get_golden_set_version(version_name)

        offset = 0
        limit = 20

        while True:
            interactions = self.api.get_interactions(golden_set_version["id"], limit=limit, offset=offset)
            for interaction in interactions:
                yield GoldenSetInteraction(id=interaction["id"],
                                           ext_interaction_id=interaction.get("ext_interaction_id"),
                                           input=interaction["input"]["data"] if interaction.get("input") else None,
                                           information_retrieval=interaction["information_retrieval"]["data"] if interaction.get("information_retrieval") else None,
                                           full_prompt=interaction["prompt"]["data"] if interaction.get("prompt") else None,
                                           output=interaction["output"]["data"] if interaction.get("output") else None,
                                           created_at=interaction["created_at"],
                                           topic=interaction["topic"],
                                           output_properties=interaction["output_properties"] if interaction.get("output_properties") else [])

            # If the size of the data is less than the limit, we've reached the end
            if len(interactions) < limit:
                break

            offset += limit

    @handle_exceptions(init_logger)
    def golden_set(self, version_name: t.Union[str, None] = None, return_topics: bool = False,
                   return_output_props: bool = False, return_annotation_data: bool = False) -> t.Union[pd.DataFrame, None]:
        """
        Fetch all the interactions from the golden set (EnvType.EVAL) as pandas dataframe

        Parameters
        ----------
        version_name : str
            version name to fetch interactions from, if no version name was supplied
            the latest created version in the application will be used (mostly useful
            when integrating the golden set rerun in the CI)

        return_topics : bool
            include topic in the data

        return_output_props : bool
            include output properties in the data

        return_annotation_data : bool
            include annotation info in the data

        Returns
        -------
        Pandas dataframe or None in case of a problem retrieving the data

        """
        golden_set_version = self._get_golden_set_version(version_name)
        csv_as_text = self.api.get_interactions_csv(golden_set_version["id"],
                                                    return_topics=return_topics,
                                                    return_output_props=return_output_props,
                                                    return_annotation_data=return_annotation_data)
        data = StringIO(csv_as_text)
        return pd.read_csv(data)

    @handle_exceptions(init_logger)
    def golden_set_generation_completed(self):
        """
        This function indicate deepchecks that golden set generation completed
        It helps to finalize golden set related actions, for instance: train topics
        model and extract topics (the model will be used later on to extract topics
        from production data)

        Returns
        -------
        None

        """
        self.api.generate_topics()

    def _get_golden_set_version(self, version_name):

        app = self.api.get_application(self.api.get_app_name())
        if not app:
            raise DeepchecksLLMClientError(f"Application: '{self.api.get_app_name()}', does not exist")
        if version_name:
            golden_set_version = next((ver for ver in app["versions"] if ver["name"] == version_name), None)
            if not golden_set_version:
                raise DeepchecksLLMClientError(f"Could not find version '{version_name}', in application '{self.api.get_app_name()}'")
        else:
            golden_set_version = max(app["versions"], key=lambda x: x['created_at'])
            if not golden_set_version:
                raise DeepchecksLLMClientError(f"Could not find versions to select from in application '{self.api.get_app_name()}'")
        return golden_set_version


# LLM Client publicly accessed singleton
dc_client: DeepchecksLLMClient = DeepchecksLLMClient()
