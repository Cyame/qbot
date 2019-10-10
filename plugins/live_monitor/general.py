import requests
from requests.adapters import HTTPAdapter
from datetime import datetime, timezone, timedelta
from typing import List


class BaseChannel:
    TIME_PRE = timedelta(minutes=5)
    requests.Session().mount('https://', HTTPAdapter(max_retries=0))

    def __init__(self, cid: str, name: str):
        self.api_url: str = ''
        self.live_url: str = ''
        self.live_status: str = '1'
        self.title: str = ''
        self.ch_name: str = ''  # 频道名，自动获取
        self.cid: str = cid
        self.name: str = name  # 频道名，手动录入
        self.get_url()
        self.last_check: datetime = datetime.now(timezone(timedelta(hours=8))) - self.TIME_PRE

        self.sendto: List[str] = []

    def get_url(self):
        self.api_url: str = ''
        self.live_url: str = ''

    def update(self) -> bool:
        if self.live_status != '1':
            self.get_status()
            if self.live_status == '1':
                return True
        elif datetime.now(timezone(timedelta(hours=8))) - self.last_check >= self.TIME_PRE:
            self.get_status()
        return False

    def get_status(self):
        html_s = requests.get(self.api_url, timeout=10).text
        self.resolve(html_s)
        if self.live_status == '1':
            self.last_check = datetime.now(timezone(timedelta(hours=8)))  # 当前时间

    def resolve(self, string: str):
        #     live_status: str
        #     title: str
        #     must be updated
        pass

    def notify(self) -> str:
        if self.live_status == '1':
            msg = f'{self.name if self.name else self.ch_name}:{self.title} {self.live_url}'
        else:
            msg = f'{self.name if self.name else self.ch_name}未开播'
        return msg

    def __str__(self):
        msg = f'Name: {self.ch_name if self.ch_name else self.name}\n' \
              f'Title: {self.title}\n' \
              f'Live Status: {self.live_status}\n'
        return msg
