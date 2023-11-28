import ctypes
import os
from pathlib import Path

from .errors import AtomikError, FileAlreadyExistsError, InvalidCrossDeviceError
from os import strerror, fsencode

from .flags import Flag

libc = ctypes.CDLL("libc.so.6", use_errno=True)


_linux_flag = {
    # Equivalent to rename # https://man7.org/linux/man-pages/man2/rename.2.html
    Flag.RENAME: 0,
    # Value copied from
    # https://github.com/torvalds/linux/blob/9bacdd8996c77c42ca004440be610692275ff9d0/include/uapi/linux/fs.h#L50
    Flag.RENAME_NOREPLACE: 1,
    Flag.RENAME_EXCHANGE: 2,
}


_FILE_EXIST = 17
_INVALID_CROSS_DEVICE = 18

_AT_FDCWD = -100


def _rename(src_path: str, dst_path: str, flag: Flag = Flag.RENAME_NOREPLACE) -> None:
    linux_flag = _linux_flag.get(flag)

    code = libc.renameat2(
        _AT_FDCWD,
        fsencode(src_path),
        _AT_FDCWD,
        fsencode(dst_path),
        linux_flag,
    )
    if code == 0:
        return
    else:
        errno = ctypes.get_errno()
        if errno == _FILE_EXIST:
            raise FileAlreadyExistsError(strerror(errno))
        if errno == _INVALID_CROSS_DEVICE:
            src_dev = os.stat(src_path).st_dev
            dst_dev = os.stat(Path(dst_path).parent).st_dev
            raise InvalidCrossDeviceError(
                f"{strerror(errno)} '{src_path}' -> '{dst_path}' ({src_dev} != {dst_dev})"
            )
        raise AtomikError(f"Error during rename: {strerror(errno)}({errno})")
