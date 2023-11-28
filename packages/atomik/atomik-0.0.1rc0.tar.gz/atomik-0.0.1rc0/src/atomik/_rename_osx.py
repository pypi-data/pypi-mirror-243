import ctypes
from .errors import AtomikError, FileAlreadyExistsError
from os import strerror, fsencode

from .flags import Flag

libc = ctypes.CDLL("libc.dylib", use_errno=True)

_osx_flag = {
    # Equivalent to rename # https://man7.org/linux/man-pages/man2/rename.2.html
    Flag.RENAME: 0,
    Flag.RENAME_NOREPLACE: 4,
    Flag.RENAME_EXCHANGE: 2,
    # Not sure of the value, taken from here https://opensource.apple.com/source/xnu/xnu-6153.41.3/bsd/sys/stdio.h
}

FILE_EXIST = 17
_AT_FDCWD = -2


def _rename(src_path: str, dst_path: str, flag: Flag = Flag.RENAME_NOREPLACE) -> None:
    osx_flag = _osx_flag.get(flag)

    code = libc.renameatx_np(
        _AT_FDCWD,
        fsencode(src_path),
        _AT_FDCWD,
        fsencode(dst_path),
        osx_flag,
    )
    if code == 0:
        return
    else:
        errno = ctypes.get_errno()
        if errno == FILE_EXIST and strerror(errno) == "File exists":
            raise FileAlreadyExistsError
        raise AtomikError(f"Error during rename: {strerror(errno)}({errno})")
