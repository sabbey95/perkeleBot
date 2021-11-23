from abc import ABC

from flask import request

from requests.channel_request import ChannelRequest


class SlashCommandRequest(ChannelRequest, ABC):
    def __init__(self):
        self.data = request.form
        super().__init__()

    def get_channel_id(self):
        return self.data.get('channel_id')
