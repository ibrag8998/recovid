from typing import NoReturn, Any, IO

from cf import get_cf

globs = get_cf('globals')


class File:
    def __init__(self, path: str, default: Any = None):
        self.path = path
        self.default = default

    def write(self, data: dict) -> NoReturn:
        with open(self.path, 'w') as f:
            self.custom_write(data, f)

    @property
    def data(self) -> dict:
        try:
            with open(self.path) as f:
                return self.custom_read(f)
        except Exception:
            return self.default

    def custom_write(self, data: dict, f: IO[str]) -> NoReturn:
        """ Abstract """
        f.write(data)

    def custom_read(self, f: IO[str]) -> str:
        """ Abstract """
        return f.read()


class CompressingFile(File):
    """ File class to perform write and read tasks.
    Compressor included for free :D.
    """
    def __init__(self, compressor_cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._compressor_cls = compressor_cls

    def custom_write(self, data: dict, f: IO[str]) -> NoReturn:
        f.write(self._compressor_cls(data).compressed_data)

    def custom_read(self, f: IO[str]) -> dict:
        return self._compressor_cls(f.read()).decompressed_data
