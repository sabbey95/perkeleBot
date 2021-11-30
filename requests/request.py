import logging
import os
from abc import abstractmethod, ABC

import slack
from flask import request

from database_utils import get_database_session
from network_utils import ssl_context


class Request(ABC):
    def __init__(self):
        self.session = get_database_session()
        self.data = request.form
        self.client = slack.WebClient(os.environ['SLACK_TOKEN'], ssl=ssl_context)

    def handle(self):
        self.session.begin()
        try:
            response = self.handle_session()
            self.session.commit()
        except Exception as e:
            logging.error(e)
            response = 'Request failed', 500
        finally:
            self.session.close()
        return response

    @abstractmethod
    def handle_session(self,):
        pass

