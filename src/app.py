from bot import Bot
from get_data import get_data
from cf import get_cf
from setup_datafiles import setup_datafiles


class App:
    data, diff = get_data()

    def __init__(self, proxy: str = None):
        self.bot = Bot(self._token, proxy=proxy)
        setup_datafiles()

    def send(self):
        self.bot.send_messages(self.data, self.diff)

    @property
    def _token(self) -> str:
        try:
            with open(get_cf('files').token) as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError("You should write your token in"
                                    " `base_dir`/token file as plain text")


app = App(proxy='http://167.71.201.161:8080')
app.send()
