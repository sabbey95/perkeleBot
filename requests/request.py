import os
from abc import abstractmethod, ABC

import slack
from flask import request, jsonify

from network_utils import ssl_context
from database import find_channel
from database_utils import get_database_session


class Request(ABC):
    def __init__(self):
        self.session = get_database_session()
        self.data = request.form
        self.client = slack.WebClient(os.environ['SLACK_TOKEN'], ssl=ssl_context)

    def handle(self):
        channel_id = self.get_channel_id()
        session = get_database_session()
        channel = find_channel(session, channel_id)

        if channel is None:
            response = self.handle_no_channel(channel_id)
        else:
            response = self.handle_channel(channel)
        self.session.commit()
        return response

    def handle_no_channel(self, channel_id):
        return jsonify({"text": "This channel is not configured for Perkeles. Try /launch-perkele-bot first."}), 200

    @abstractmethod
    def handle_channel(self, channel):
        pass

    @abstractmethod
    def get_channel_id(self):
        pass
