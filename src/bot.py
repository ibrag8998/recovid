from datetime import datetime
from typing import NoReturn

import httpx

from filework import CompressingFile
from compressors import ChatsCompressor, OffsetCompressor
from cf import get_cf

files = get_cf('files')  # Idk how to do in better way
defaults = get_cf('defaults')
bot_config = get_cf('bot')


class Bot:
    chatsfile = CompressingFile(compressor_cls=ChatsCompressor,
                                path=files.chats,
                                default=defaults.chats)
    offsetfile = CompressingFile(compressor_cls=OffsetCompressor,
                                 path=files.offset,
                                 default=defaults.offset)

    message_text = bot_config.message_text

    def __init__(self, token: str, debug: bool = False, proxy: str = None):
        self.url = f'https://api.telegram.org/bot{token}'
        self.debug = debug
        self.proxies = {'https': proxy} if proxy else None

    def send_messages(self, data: dict, diff: dict) -> NoReturn:
        self._update_chats()
        self.message_text = self.message_text.format(
            datetime.now().strftime('%Y-%m-%d'),
            *(data['world']['cases'], diff['world']['cases']),
            *(data['ru']['cases'], diff['ru']['cases']),
            *(data['dag']['cases'], diff['dag']['cases']),
            *(data['world']['deaths'], diff['world']['deaths']),
            *(data['ru']['deaths'], diff['ru']['deaths']),
            *(data['dag']['deaths'], diff['dag']['deaths']),
            *(data['world']['cured'], diff['world']['cured']),
            *(data['ru']['cured'], diff['ru']['cured']),
            *(data['dag']['cured'], diff['dag']['cured']),
        )

        chats = (bot_config.debug_chat, )
        if not self.debug:
            chats = self.chatsfile.data
        sent = []

        for chat_id in chats:
            if chat_id not in sent:
                self._send_message(chat_id)
                sent.append(chat_id)

    def _send_message(self, chat_id: str) -> NoReturn:
        self._mkreq('sendMessage', chat_id=chat_id, text=self.message_text)

    def _mkreq(self, method: str, **kwargs) -> dict:
        """ Make request. """
        with httpx.Client(proxies=self.proxies) as client:
            return client.get(f'{self.url}/{method}',
                              params=kwargs,
                              timeout=10.0).json()

    def _update_chats(self) -> NoReturn:
        updates = self._mkreq('getUpdates', offset=self.offsetfile.data)
        chats = self.chatsfile.data
        for update in updates['result']:
            offset = update['update_id']
            chat = update.get('message', update.get('edited_message'))['chat']
            if chat['type'] in ('group', 'supergroup'):
                if str(chat['id']) not in chats:
                    chats.append(chat['id'])

        self.chatsfile.write(chats)
        self.offsetfile.write(offset)
