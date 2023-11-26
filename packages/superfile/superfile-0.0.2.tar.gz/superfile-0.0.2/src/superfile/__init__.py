from typing import Iterable
from . import interfaces
from . import amazon_simple_storage_service
from . import google_cloud_storage


_SCHEME_MAPPING = {
    google_cloud_storage.GCSFile.scheme: google_cloud_storage.GCSFile,
    amazon_simple_storage_service.S3File.scheme: amazon_simple_storage_service.S3File,
}


def _infer_client(path: str, **kwargs) -> interfaces.SuperFile:
  scheme, _ = path.split("://", 1)
  return _SCHEME_MAPPING[scheme](**kwargs)


def open(
    path: str,
    mode: interfaces.FileMode = "r",
    init_kwargs: dict | None = None,
    open_kwargs: dict | None = None,
) -> interfaces.FileLike:
  client = _infer_client(path, **(init_kwargs or {}))
  return client.open(path, mode, **(open_kwargs or {}))


def list(
    path: str,
    init_kwargs: dict | None = None,
    list_kwargs: dict | None = None,
) -> Iterable[str]:
  client = _infer_client(path, **(init_kwargs or {}))
  return client.list(path, **(list_kwargs or {}))
