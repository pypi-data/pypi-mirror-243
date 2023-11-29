"""
User facing methods on the dfl object of core sdk
"""

import logging

from .attacks import pii_extraction
from .datasets.dataset import Dataset
from .logging import set_logger
from .MessageHandler import _MessageHandler
from .models import local_model, remote_model
from .State import _State
from .tests.gpu_config import GPUSpecification
from .tests.test import Test
from .vector_db import ChromaDB

try:
    from typing import Optional
except ImportError:
    from typing_extensions import Optional


RETRY_AFTER = 5  # seconds


class DynamoFL:
    """Creates a client instance that communicates with the API through REST and websockets.

    Args:
        token - Your auth token. Required.

        host - API server url. Defaults to DynamoFL prod API.

        metadata - Sets a default metadata object for attach_datasource calls; can be overriden.

        log_level - Set the log_level for the client.
            Accepts all of logging._Level. Defaults to logging.INFO.
    """

    def __init__(
        self,
        token: str,
        host: str = "https://api.dynamofl.com",
        metadata: object = None,
        log_level=logging.INFO,
    ):
        self._state = _State(token, host, metadata)
        self._messagehandler = _MessageHandler(self._state)
        self._messagehandler.connect_to_ws()

        set_logger(log_level=log_level)

    def attach_datasource(self, key, train=None, test=None, name=None, metadata=None):
        return self._state.attach_datasource(
            key, train=train, test=test, name=name, metadata=metadata
        )

    def delete_datasource(self, key):
        return self._state.delete_datasource(key)

    def get_datasources(self):
        return self._state.get_datasources()

    def delete_project(self, key):
        return self._state.delete_project(key)

    def get_user(self):
        return self._state.get_user()

    def create_project(
        self,
        base_model_path,
        params,
        dynamic_trainer_key=None,
        dynamic_trainer_path=None,
    ):
        return self._state.create_project(
            base_model_path,
            params,
            dynamic_trainer_key=dynamic_trainer_key,
            dynamic_trainer_path=dynamic_trainer_path,
        )

    def get_project(self, project_key):
        return self._state.get_project(project_key)

    def get_projects(self):
        return self._state.get_projects()

    def is_datasource_labeled(self, project_key=None, datasource_key=None):
        """
        Accepts a valid datasource_key and project_key
        Returns True if the datasource is labeled for the project; False otherwise

        """
        return self._state.is_datasource_labeled(
            project_key=project_key, datasource_key=datasource_key
        )

    def upload_dynamic_trainer(self, dynamic_trainer_key, dynamic_trainer_path):
        return self._state.upload_dynamic_trainer(dynamic_trainer_key, dynamic_trainer_path)

    def download_dynamic_trainer(self, dynamic_trainer_key):
        return self._state.download_dynamic_trainer(dynamic_trainer_key)

    def delete_dynamic_trainer(self, dynamic_trainer_key):
        return self._state.delete_dynamic_trainer(dynamic_trainer_key)

    def get_dynamic_trainer_keys(self):
        return self._state.get_dynamic_trainer_keys()

    def create_attack(self):
        return pii_extraction.PIIExtraction(self._state.request)

    def create_test(
        self,
        name: str,
        model_key: str,
        dataset_id: str,
        test_type: str,
        gpu: GPUSpecification,
        config: list,
        api_key=None,
    ):
        return Test(
            request=self._state.request,
            name=name,
            model_key=model_key,
            dataset_id=dataset_id,
            test_type=test_type,
            gpu=gpu,
            config=config,
            api_key=api_key,
        )

    def create_rag_test(
        self,
        name: str,
        model_key: str,
        dataset_id: str,
        gpu: GPUSpecification,
        prompt_template: str,
        config: list,
        vector_db: ChromaDB,
        retrieve_top_k: int,
        rag_hallucination_metrics: list[str],
        api_key=None,
    ):
        for c in config:
            c["dataset"]["prompt_template"] = prompt_template
            c["attack"]["rag_hallucination_metrics"] = rag_hallucination_metrics
            c["attack"]["retrieve_top_k"] = retrieve_top_k
            c["dataset"]["vector_db"] = vector_db.__dict__

        return self.create_test(
            name, model_key, dataset_id, "rag-hallucination-test", gpu, config, api_key
        )

    def get_use_cases(self):
        self._state.get_use_cases()

    def get_test_info(self, test_id: str):
        return self._state.get_test_info(test_id)

    def get_attack_info(self, attack_id: str):
        return self._state.get_attack_info(attack_id)

    def get_datasets(self):
        self._state.get_datasets()

    def create_centralized_project(
        self,
        name,
        datasource_key,
        rounds=None,
        use_case_key=None,
        use_case_path=None,
    ):
        self._state.create_centralized_project(
            name,
            datasource_key,
            rounds=rounds,
            use_case_key=use_case_key,
            use_case_path=use_case_path,
        )

    def create_model(
        self,
        model_file_path: str,
        name: str,
        config: object,
        key: Optional[str] = None,
        peft_config_path: Optional[str] = None,
    ):
        return local_model.LocalModel.create_and_upload(
            request=self._state.request,
            name=name,
            key=key,
            model_file_path=model_file_path,
            config=config,
            peft_config_path=peft_config_path,
        )

    def create_remote_model(
        self,
        name: str,
        api_provider: str,
        api_instance: str,
        key: str,
        endpoint: Optional[str] = None,
    ):
        return remote_model.RemoteModel.create_and_upload(
            request=self._state.request,
            name=name,
            key=key,
            api_provider=api_provider,
            api_instance=api_instance,
            endpoint=endpoint,
        )

    def get_model(self, key: str):
        return self._state.get_model(key)

    def create_dataset(self, file_path, key: str = None, name: str = None):
        return Dataset(request=self._state.request, name=name, key=key, file_path=file_path)
