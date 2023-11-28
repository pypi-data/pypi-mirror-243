import contextlib
import os
import shutil
import tempfile
from enum import Enum
from pathlib import Path
from typing import Optional, Generator, IO, Union, Any

from .flags import Flag
from .rename import rename


class Mode(str, Enum):
    TEXT = "TEXT"
    BYTES = "BYTES"


@contextlib.contextmanager
def file(
    file_name: Union[str, Path],
    mode: Mode = Mode.TEXT,
    overwrite: bool = False,
    tmp_dir: Optional[Union[str, Path]] = None,
) -> Generator[IO[Any], None, None]:
    # raise if filename ends with / ?
    # raise if tmp_dir doesn't exist ?
    fd, name = tempfile.mkstemp(dir=tmp_dir, suffix=".atomik")

    src = str(Path(name).absolute())
    dst = str(Path(file_name).absolute())
    f = os.fdopen(fd, "wt" if mode == Mode.TEXT else "wb")
    yield f
    f.close()

    flag = Flag.RENAME if overwrite else Flag.RENAME_NOREPLACE
    rename(src, dst, flag)


@contextlib.contextmanager
def folder(
    file_name: Union[str, Path],
    overwrite: bool = False,
    tmp_dir: Optional[Union[str, Path]] = None,
) -> Generator[Path, None, None]:
    name = tempfile.mkdtemp(dir=tmp_dir, suffix=".atomik")

    src = str(Path(name).absolute())
    dst = str(Path(file_name).absolute())

    yield Path(name)

    if overwrite:
        rename(src, dst, Flag.RENAME_EXCHANGE)
        shutil.rmtree(src)
    else:
        rename(src, dst)
