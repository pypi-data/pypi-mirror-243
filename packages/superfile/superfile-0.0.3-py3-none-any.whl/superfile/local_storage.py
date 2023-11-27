import pathlib
from typing import Iterable

from . import interfaces


def _filter_files(paths: Iterable[pathlib.Path]) -> Iterable[str]:
  yield from (str(x.absolute()) for x in paths if x.is_file())


class LocalFile(interfaces.SuperFile):
  scheme = "file"

  def __init__(self, **kwargs):
    pass

  def open(
      self,
      path: str,
      mode: interfaces.FileMode = "r",
      encoding: str | None = None,
      **kwargs,
  ) -> interfaces.FileLike:
    uri = interfaces.FileURI.from_url(path, validate_scheme=LocalFile.scheme)
    return open(uri.subpath, mode=mode, encoding=encoding, **kwargs)

  def list(self, path: str, **kwargs) -> Iterable[str]:
    uri = interfaces.FileURI.from_url(path, validate_scheme=LocalFile.scheme)
    subpath = pathlib.Path(uri.subpath)
    if subpath.is_dir():
      yield from _filter_files(subpath.rglob("*"))
    else:
      pattern = subpath.name + ("" if "*" in subpath.name else "*")
      yield from _filter_files(subpath.parent.rglob(pattern))
