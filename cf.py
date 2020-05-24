""" Configuration module """
import os

base_dir = os.path.dirname(os.path.abspath(__file__))


def get_cf(cf):
    """ Get specified configuration class """
    switch = {'files': FilesConfig, 'globals': GlobalsConfig}
    return switch[cf]


class FilesConfig:
    data = os.path.join(base_dir, 'Datafile')


class GlobalsConfig:
    scopes = ('world', 'ru', 'dag')
    cats = ('cases', 'deaths', 'cured')
    url = 'https://yandex.ru/maps/api/covid?ajax=1'
