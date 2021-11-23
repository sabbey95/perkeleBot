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
        self.session.begin()
        response = self.handle_session()
        self.session.commit()
        self.session.close()
        return response

    @abstractmethod
    def handle_session(self,):
        pass

