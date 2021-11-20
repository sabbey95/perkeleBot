import threading

import schedule

from database import Channel
from database_utils import new_database_session
from requests.board_of_shame_request import send_board_of_shame
from scheduled_tasks.perkele_checker import PerkeleChecker


def schedule_tasks(client):
    schedule.every(60).seconds.do(PerkeleChecker(client).run)
    schedule.every().monday.at("09:00").do(send_leader_board_updates, client)
    run_scheduled_tasks()


def run_scheduled_tasks():
    schedule.run_pending()
    t = threading.Timer(60, run_scheduled_tasks)
    t.start()


def send_leader_board_updates(client):
    session = new_database_session()
    channels = session.query(Channel).all()
    for channel in channels:
        send_board_of_shame(client, channel, session)
