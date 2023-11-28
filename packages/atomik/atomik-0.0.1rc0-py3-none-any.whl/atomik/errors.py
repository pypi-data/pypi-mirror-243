class AtomikError(Exception):
    pass


class FileAlreadyExistsError(AtomikError):
    pass


class InvalidCrossDeviceError(AtomikError):
    pass
