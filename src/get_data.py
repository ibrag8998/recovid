from typing import Tuple

import httpx

from filework import CompressingFile
from compressors import DataCompressor
from cf import get_cf

globs = get_cf('globals')


class DataRelated:
    @property
    def data(self):
        raise NotImplementedError


class DataCollectorDecorator(DataRelated):
    @staticmethod
    def _get_from_outside():
        raise NotImplementedError

    def _parse(self, raw):
        raise NotImplementedError

    @property
    def data(self):
        return self._parse(self._get_from_outside())


class DataCollectorYandex(DataCollectorDecorator):
    @staticmethod
    def _get_from_outside():
        """ Pass csrf_token auth and get whole raw json.

        The mechanism is:
        I make GET req to the url, it returns json where only csrf_token
        is present, then I extract it and make new req within same session,
        but change csrf_token in url query string to the new one, and it
        returns needed information
        """
        client = httpx.Client()
        # make req to get csrf_token and extract it
        token = client.get(globs.url).json()['csrfToken']
        # now make req with this token in query string
        resp = client.post(globs.url, params={'csrfToken': token}).json()
        return resp

    def _parse(self, raw):
        data = {
            scope: {cat: 0
                    for cat in globs.cats}
            for scope in globs.scopes
        }

        for item in raw['data']['items']:
            for cat in globs.cats:
                # if dag, add to data['dag']
                if item['name'] == 'Республика Дагестан':
                    data['dag'][cat] += item[cat] or 0

                # if ru, also add to data['ru']
                if item.get('ru'):
                    data['ru'][cat] += item[cat] or 0

                # anyway add to data['world']
                data['world'][cat] += item[cat] or 0

        return data


class DataDifference(DataRelated):
    def __init__(self, collector, storage):
        self.cur = collector.data
        self.prev = storage.data

    @property
    def diff(self):
        """ Calculate difference between current and previous data """
        return {
            scope: {
                cat: self.cur[scope][cat] - self.prev[scope][cat]
                for cat in globs.cats
            }
            for scope in globs.scopes
        }

    @property
    def data(self):
        return self.cur, self.diff


def get_data() -> Tuple[dict, dict]:
    """ Main """
    datafile = CompressingFile(compressor_cls=DataCompressor,
                               path=get_cf('files').data,
                               default=get_cf('defaults').data)
    cur, diff = DataDifference(DataCollectorYandex(), datafile).data
    datafile.write(cur)
    return cur, diff


if __name__ == "__main__":  # testing purposes
    print(get_data())
