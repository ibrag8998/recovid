""" Collect all required data, e.g. current data about World, Russia, Dagestan
and also difference between current and yesterday's data
"""
import requests

from filework import write_data, read_data
from cf import get_cf


def get_json():
    """ Pass csrf_token auth ans get whole raw json """
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


def get_cur_data():
    """ Get current data about World, Russia and Dagestan """
    # get full raw json data to extract info from
    full_data = get_json()
    # construct skeleton of returning dict
    data = {scope: {cat: 0 for cat in cats} for scope in scopes}

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


def calc_diff(cur, prev):
    """ Calculate difference between current and previous data """
    return {
        scope: {cat: cur[scope][cat] - prev[scope][cat]
                for cat in cats}
        for scope in scopes
    }


def main():
    """ Main """
    prev_data = read_data()
    cur_data = get_cur_data()

    diff = calc_diff(cur_data, prev_data)

    write_data(cur_data)
    return cur_data, diff


globs = get_cf('globals')
url, scopes, cats = globs.url, globs.scopes, globs.cats

if __name__ == "__main__":
    print(main())
