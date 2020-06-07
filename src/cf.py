import os


def get_cf(cf):
    """ Get specified configuration class """
    switch = {
        'files': FilesConfig,
        'globals': GlobalsConfig,
        'defaults': DefaultsConfig,
        'bot': BotConfig,
    }
    return switch[cf]


class FilesConfig:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_dir = os.path.join(base_dir, 'src')
    datafiles_dir = os.path.join(base_dir, 'data')
    data = os.path.join(datafiles_dir, 'Datafile')
    chats = os.path.join(datafiles_dir, 'Chatsfile')
    offset = os.path.join(datafiles_dir, 'Offsetfile')
    token = os.path.join(base_dir, 'token')


class GlobalsConfig:
    scopes = ('world', 'ru', 'dag')
    cats = ('cases', 'deaths', 'cured')
    url = 'https://yandex.ru/maps/api/covid?ajax=1'


class DefaultsConfig:
    data = {
        scope: {cat: 0
                for cat in GlobalsConfig.cats}
        for scope in GlobalsConfig.scopes
    }
    chats = []
    offset = 1


class BotConfig:
    debug_chat = '-317873756'
    message_text = ("Дата: {}\n\n"
                    "Заражений:\n"
                    "- Мир: {} (+{})\n"
                    "- Россия: {} (+{})\n"
                    "- Дагестан: {} (+{})\n\n"
                    "Смертей:\n"
                    "- Мир: {} (+{})\n"
                    "- Россия: {} (+{})\n"
                    "- Дагестан: {} (+{})\n\n"
                    "Выздоровлений:\n"
                    "- Мир: {} (+{})\n"
                    "- Россия: {} (+{})\n"
                    "- Дагестан: {} (+{})\n\n"
                    "Будьте осторожны! Берегите себя и свои семьи!\n\n"
                    "Подписывайся на канал @seytuevru")
