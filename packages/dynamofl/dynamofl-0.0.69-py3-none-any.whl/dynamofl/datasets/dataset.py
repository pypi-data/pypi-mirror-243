"""Dataset class for Dynamofl."""

from ..file_transfer.upload import FileUploader
from ..Request import _Request
from .base_dataset import BaseDataset

CHUNK_SIZE = 1024 * 1024  # 1MB


class Dataset(BaseDataset):
    """Dataset class for Dynamofl."""

    def __init__(self, request: _Request, name: str, key: str, file_path: str) -> None:
        self.request = request
        upload_op = self.upload_dataset_file(key=key, dataset_file_path=file_path)
        obj_key = upload_op["objKey"]
        key = upload_op["entityKey"]
        config = {"objKey": obj_key}
        super().__init__(request=request, name=name, key=key, config=config)

    def upload_dataset_file(self, key: str, dataset_file_path: str):
        file_uploader = FileUploader(self.request)
        response = file_uploader.upload_file(
            file_path=dataset_file_path,
            presigned_endpoint_url="/dataset/presigned-url",
            construct_params=lambda params_args: {
                "key": key,
                "sha1Checksum": params_args.sha1hash,
                "filename": params_args.file_name,
            },
        )
        return response.presigned_endpoint_response
