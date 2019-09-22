__all__ = ['bili', 'cc', 'general', 'youtube', 'Monitor']

from plugins.live_monitor.general import Channel as BaseChannel
from plugins.live_monitor.youtube import YoutubeChannel
from plugins.live_monitor.bili import BiliChannel
from plugins.live_monitor.cc import NetEaseChannel
import json


def init_channel(channel_type, cid: str, name: str):
    if channel_type == 'bili':
        return BiliChannel(cid, name)
    elif channel_type == 'you':
        return YoutubeChannel(cid, name)
    elif channel_type == 'cc':
        return NetEaseChannel(cid, name)


class Monitor:
    channel_list: list = []
    debug = False
    pos = -1
    notify = print

    def __init__(self, channel_type: str, debug=False):
        assert channel_type in ['bili', 'you', 'cc']
        self.channel_type = channel_type
        self.debug = debug

    def init_channel(self, cid: str, name: str):
        if self.channel_type == 'bili':
            return BiliChannel(cid, name)
        elif self.channel_type == 'you':
            return YoutubeChannel(cid, name)
        elif self.channel_type == 'cc':
            return NetEaseChannel(cid, name)

    def add(self, cid: str, name: str):
        ch = self.init_channel(cid, name)
        if ch.cid not in [ch.id for ch in self.channel_list]:
            self.channel_list.append(ch)

    def remove(self, cid: str):
        for ch in self.channel_list:
            if ch.id == cid:
                self.channel_list.remove(ch)

    def load(self):
        try:
            with open(self.channel_type + '.json', 'r') as f:
                channel_json = json.load(f)
            [self.add(ch_j['id'], ch_j['name']) for ch_j in channel_json]
        except FileNotFoundError:
            pass

    def save(self):
        channel_json = [{'id': ch.id, 'name': ch.name} for ch in self.channel_list]
        with open(self.channel_type + '.json', 'w') as f:
            json.dump(channel_json, f, indent=2, ensure_ascii=False)

    def next(self):
        if self.channel_list:
            self.pos = self.pos + 1 if self.pos < len(self.channel_list) - 1 else 0
            return self.channel_list[self.pos]
        else:
            return None

    def run(self) -> str:
        channel: BaseChannel = self.next()
        if channel and (channel.update() or self.debug):
            return channel.notify()

    def __str__(self):
        msg = ''
        for ch in self.channel_list:
            msg += str(ch)
        return msg
