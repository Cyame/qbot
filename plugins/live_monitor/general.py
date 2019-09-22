import requests
from datetime import datetime, timezone, timedelta


class Channel:
    TIME_PRE = timedelta(minutes=5)
    last_check: datetime
    api_url: str = ''
    live_url: str = ''
    id: str = ''
    name: str = ''
    live_status: str = '1'
    title: str = ''
    ch_name: str = ''

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.get_url()
        self.last_check = datetime.now(timezone(timedelta(hours=8))) - self.TIME_PRE
        return

    def get_url(self):
        self.api_url = ''
        self.live_url = ''

    def update(self) -> bool:
        if self.live_status != '1':
            self.get_status()
            if self.live_status == '1':
                return True
        elif datetime.now(timezone(timedelta(hours=8))) - self.last_check >= self.TIME_PRE:
            self.get_status()
        return False

    def get_status(self):
        html_s = requests.get(self.api_url).text
        self.resolve(html_s)
        if self.live_status == '1':
            self.last_check = datetime.now(timezone(timedelta(hours=8)))  # 当前时间

    def resolve(self, string: str):
        #     live_status: str
        #     title: str
        #     must be updated
        pass

    def __str__(self):
        msg = f'Name: {self.ch_name if self.ch_name else self.name}\n' \
              f'Title: {self.title}\n' \
              f'Live Status: {self.live_status}\n'
        return msg

    def notify(self):
        if self.live_status == '1':
            msg = f'{self.name}:{self.title} {self.live_url}'
        else:
            msg = f'{self.name}未开播'
        return msg
