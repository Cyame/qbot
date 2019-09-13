#!/usr/bin/python

import urllib.request
import json
import nonebot
from datetime import datetime, timezone, timedelta
from plugins.monitor_bili.config import channel_list_bili, TIME_PRE
from utils_bot.msg_ops import send_to_groups

__plugin_name__ = '监控器_bili'
__plugin_usage__ = r'''feature: 监控器_bili
监视bilibili开播状态并自动提醒
'''

bot = nonebot.get_bot()


class Channel:
    live_status: int = 0
    live_time: str = '0000-00-00 00:00:00'  # 本次开播时间
    # last_live: str = '1970-01-02 00:00:00'  # 上次下播时间
    # last_check: str = '1970-01-02 00:00:00'  # 上次检测到直播时间

    def __init__(self, room_id, name):
        self.room_id: str = room_id  # 直播间房间号
        self.name: str = name
        self.live_url: str = f'https://api.live.bilibili.com/room/v1/Room/get_info?id={room_id}'
        self.last_check = (datetime.now(timezone(timedelta(hours=8))) - TIME_PRE).strftime('%Y-%m-%d %H:%M:%S')

    def update(self):
        # 获取信息
        json_s = urllib.request.urlopen(self.live_url).read().decode('utf-8')
        json_d = json.loads(json_s)
        self.live_status = json_d.get('data').get('live_status')
        self.live_time = json_d.get('data').get('live_time')
        # 距离上次下播大于time_pre
        if self.time_delta(self.live_time, self.last_check) > TIME_PRE:
            ret = 1
        else:
            ret = 0
        # 开播状态
        if self.live_status == 1:
            self.last_check = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')  # 当前时间
            # self.last_live = self.last_check
        return ret

    @staticmethod
    def time_delta(ta, tb):
        if ta == '0000-00-00 00:00:00':
            a = datetime.fromtimestamp(0)
        else:
            a: datetime = datetime.strptime(ta, "%Y-%m-%d %H:%M:%S")
        b: datetime = datetime.strptime(tb, "%Y-%m-%d %H:%M:%S")
        delta: timedelta = a - b
        return delta

    def __str__(self):
        msg = f'Channel Name: {self.name}\n'
        self.update()
        msg += f'Live Status: {self.live_status}\n'
        msg += f'URL: https://live.bilibili.com/{self.room_id}'
        return msg


def circle(n):
    x = 0
    while True:
        yield x
        x = x + 1 if x < n - 1 else 0


channels = [Channel(room_id, name) for room_id, name in channel_list_bili]
v = circle(len(channels))


@nonebot.scheduler.scheduled_job('interval', seconds=2.5)
async def _():
    channel = channels[next(v)]
    if channel.update():
        if channel.live_status == 1:
            msg = f'{channel.name}于{channel.live_time[11:16]}开播了: '
            msg += f'https://live.bilibili.com/{channel.room_id}'
            await send_to_groups(msg)
