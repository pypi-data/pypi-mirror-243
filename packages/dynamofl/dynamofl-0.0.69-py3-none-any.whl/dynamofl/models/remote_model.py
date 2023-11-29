"""DynamoFL Remote Model"""
from ..models.model import Model
from ..Request import _Request

try:
    from typing import Optional
except ImportError:
    from typing_extensions import Optional


class RemoteModel(Model):
    """RemoteModel"""

    def __init__(
        self,
        request,
        name: str,
        key: str,
        model_id: str,
        config,
    ) -> None:
        self.request = request
        super().__init__(
            request=request,
            name=name,
            key=key,
            config=config,
            model_type="REMOTE",
            model_id=model_id,
        )

    @staticmethod
    def create_and_upload(
        request: _Request,
        name: str,
        key: str,
        api_provider: str,
        api_instance: str,
        endpoint: Optional[str],
    ):
        config = {
            "remoteModelApiProvider": api_provider,
            "remoteModelApiInstance": api_instance,
            "remoteModelEndpoint": endpoint,
        }

        model_id = Model.create_ml_model_and_get_id(
            request=request, name=name, key=key, model_type="REMOTE", config=config, size=None
        )

        return RemoteModel(
            request=request,
            name=name,
            key=key,
            config=config,
            model_id=model_id,
        )
