""" Module for all file-related stuff functions, such as write, read, etc """
from cf import get_cf


def compress(data: dict):
    """ Compress data.

    Structure of :param data: looks like:
    {`scope`: {`category`: `num`}}

    Compressed structure:
    '`num1`,`num2`,`num3`,...'

    where first 3 nums represents World's data, second 3 for Russian,
    last 3 for Dag. In each triple, first num is cases, second is deaths,
    third is cured. More details:

    <world_cases>,<world_deaths>,<world_cured>,<ru_cases>,...
    """
    return ','.join([
        str(num) for local_data in data.values()
        for num in local_data.values()
    ])


def decompress(data: str):
    """ Decompress data. See `compress()` docs """
    data = tuple(map(int, data.split(',')))
    scopes = ('world', 'ru', 'dag')
    cats = ('cases', 'deaths', 'cured')
    res = {
        scopes[i]: {cats[j]: data[i * 3 + j]
                    for j in range(3)}
        for i in range(3)
    }
    return res


def write_data(data: dict):
    """ Write data to file specified in cf.py """
    with open(datafile, 'w') as f:
        f.write(compress(data))


def read_data():
    """ Read data """
    try:
        with open(datafile) as f:
            return decompress(f.read())
    except FileNotFoundError:
        return {scope: {cat: 0 for cat in cats} for scope in scopes}


datafile = get_cf('files').data
globs = get_cf('globals')
scopes, cats = globs.scopes, globs.cats
