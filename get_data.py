"""Collect all required information, e.g. current data about World,
Russia, Dagestan, and also difference between current and yesterday's

When you see code like this:

>>> except Exception as e:
...     raise e

It means this error waits to be handled properly
"""
from pprint import pprint
import json

import requests


def get_json():
    """ Pass csrf_token auth ans get rudag json """
    try:
        # Session is required because of csrf_token. The mechanism is:
        # I make GET req to the url, it returns json where only csrf_token
        # is present, then I extract it and make new req within same session,
        # but change csrf_token in url query string to the new one, and it
        # returns needed information
        sesh = requests.Session()
        # make req to get csrf_token and extract it
        token = sesh.get(url).json()['csrfToken']
        # now make req with this token in query string
        resp = sesh.get(url, params={'csrfToken': token}).json()
        return resp
    except json.decoder.JSONDecodeError as e:
        raise e


def get_cur_data():
    """ Get current data about World, Russia and Dagestan """
    # get full raw json data to extract info from
    full_data = get_json()
    # helper tuple
    cats = ('cases', 'deaths', 'cured')
    # construct skeleton of returning dict
    data = {
        scope: {cat: 0
                for cat in cats}
        for scope in ('world', 'ru', 'dag')
    }

    for item in full_data['data']['items']:
        for cat in cats:
            # if dag, add to data['dag']
            if item['name'] == 'Республика Дагестан':
                data['dag'][cat] += item[cat]

            # if ru, also add to data['ru']
            if item.get('ru'):
                data['ru'][cat] += item[cat]

            # anyway add to data['world']
            data['world'][cat] += item[cat]

    return data


def get_data():
    """ Get whole required data: current and difference """
    cur_data = get_cur_data()
    diff = None

    return cur_data, diff


url = 'https://yandex.ru/maps/api/covid?ajax=1'
pprint(get_data())
