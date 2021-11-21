import os

import schedule
import slack

from network_utils import ssl_context
from database import Channel
from database_utils import get_database_session
from requests.board_of_shame_request import send_board_of_shame
from scheduled_tasks.perkele_checker import PerkeleChecker


def schedule_tasks():
    schedule.every(60).seconds.do(PerkeleChecker().run)
    schedule.every().monday.at("09:00").do(send_leader_board_updates)
    run_pending_tasks()


def run_pending_tasks():
    schedule.run_pending()


def send_leader_board_updates():
    session = get_database_session()
    channels = session.query(Channel).all()
    client = slack.WebClient(os.environ['SLACK_TOKEN'], ssl=ssl_context)
    for channel in channels:
        send_board_of_shame(client, channel, session)
