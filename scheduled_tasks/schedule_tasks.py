import os

import slack

from database import Channel
from database_utils import get_database_session
from network_utils import ssl_context
from requests.board_of_shame_request import send_board_of_shame


def send_leader_board_updates():
    session = get_database_session()
    channels = session.query(Channel).all()
    client = slack.WebClient(os.environ['SLACK_TOKEN'], ssl=ssl_context)
    for channel in channels:
        send_board_of_shame(client, channel, session)
