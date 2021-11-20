import os
import ssl
from pathlib import Path

import slack
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

from database import initialise_database
from requests.board_of_shame_request import BoardOfShameRequest
from requests.launch_bot_request import LaunchBotRequest
from requests.message_request import MessageRequest
from requests.set_perkele_hours_request import SetPerkeleHoursRequest
from scheduled_tasks.schedule_tasks import schedule_tasks

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
initialise_database()

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)
client = slack.WebClient(os.environ['SLACK_TOKEN'], ssl=ssl_context)

schedule_tasks(client)


@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    return MessageRequest(event).handle()


@app.route('/launch-perkele-bot', methods=['POST'])
def launch_perkele_bot():
    return LaunchBotRequest().handle()


@app.route('/set-perkele-hours', methods=['POST'])
def set_perkele_hours():
    return SetPerkeleHoursRequest().handle()


@app.route('/perkele-board-of-shame', methods=['POST'])
def perkele_board_of_shame():
    return BoardOfShameRequest(client).handle()


if __name__ == "__main__":
    app.run(debug=False)
