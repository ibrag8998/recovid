from typing import Any

from cf import get_cf

globs = get_cf('globals')


class _Compressor:
    """ Compressor class.

    Implement `compressed_data` and `decompressed_data`. You have access to
    `self.data` - data which you should compress or decompress.
    """
    def __init__(self, data: Any):
        self.data = data

    @property
    def compressed_data(self):
        raise NotImplementedError

    @property
    def decompressed_data(self):
        raise NotImplementedError


class OffsetCompressor(_Compressor):
    @property
    def compressed_data(self) -> str:
        return str(self.data)

    @property
    def decompressed_data(self) -> int:
        return int(self.data.strip())


class ChatsCompressor(_Compressor):
    @property
    def compressed_data(self) -> str:
        return '\n'.join([str(chat) for chat in self.data])

    @property
    def decompressed_data(self) -> list:
        return [
            line.strip() for line in self.data.splitlines() if line.strip()
        ]


class DataCompressor(_Compressor):
    @property
    def compressed_data(self) -> str:
        """ Structure of `self.data`, if it is a dict, looks like:
        {`scope`: {`category`: `num`}}

        Compressed structure:
        '`num1`,`num2`,`num3`,...'

        where first 3 nums represents World's data, second 3 for Russian,
        last 3 for Dag. In each triple, first num is cases, second is deaths,
        third is cured. More details:

        <world_cases>,<world_deaths>,<world_cured>,<ru_cases>,...
        """
        return ','.join([
            str(num) for local_data in self.data.values()
            for num in local_data.values()
        ])

    @property
    def decompressed_data(self) -> dict:
        """ See `compressed_data` docs. """
        data = tuple(map(int, self.data.split(',')))
        return {
            globs.scopes[i]:
            {globs.cats[j]: data[i * 3 + j]
             for j in range(3)}
            for i in range(3)
        }
