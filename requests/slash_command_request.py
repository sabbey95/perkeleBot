from abc import ABC
from flask import request

from requests.request import Request


class SlashCommandRequest(Request, ABC):
    def __init__(self):
        self.data = request.form
        super().__init__()

    def get_channel_id(self):
        return self.data.get('channel_id')
