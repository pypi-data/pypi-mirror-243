import logging

from ..Request import _Request
from .gpu_config import GPUSpecification, GPUConfig, VRAMConfig


class Test:
    def __init__(
        self,
        request: _Request,
        name: str,
        model_key: str,
        dataset_id: str,
        test_type: str,
        gpu: GPUSpecification,
        config: list,
        api_key=None,
    ) -> None:
        self.request = request
        self.name = name
        self.model_key = model_key
        self.dataset_id = dataset_id
        self.attack_type = test_type
        self.test_type = test_type
        self.gpu = gpu
        self.config = config
        self.api_key = api_key
        self.logger = logging.getLogger("Test")
        if self.gpu is None:
            raise Exception("GPU is not set.")

        if isinstance(self.gpu, VRAMConfig):
            if self.gpu.vramGB is None or self.gpu.vramGB <= 0:
                raise Exception("VRAM is not set.")

        if isinstance(self.gpu, GPUConfig):
            if self.gpu.gpu_count is None or self.gpu.gpu_type is None:
                raise Exception(
                    "GPU is not set. You need to set gpu_count and gpu_type."
                )

        params = {
            "name": name,
            "modelKey": model_key,
            "datasetId": dataset_id,
            "type": test_type,
            "gpu": gpu.as_dict(),
            "config": config,
        }
        if api_key:
            params["apiKey"] = api_key

        res = self.request._make_request("POST", "/attack/test", params=params)
        self.test_id = res["id"]
        self.attacks = res["attacks"]
        self.logger.info("Test created: {}".format(res))
