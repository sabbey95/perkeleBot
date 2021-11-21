import os

from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

import database as initialise_database
from requests.board_of_shame_request import BoardOfShameRequest
from requests.launch_bot_request import LaunchBotRequest
from requests.message_request import MessageRequest
from requests.post_config_request import PostConfigRequest
from requests.set_perkele_hours_request import SetPerkeleHoursRequest
from requests.toggle_perkele_pause import TogglePerkelePauseRequest
from scheduled_tasks.perkele_checker import PerkeleChecker
from scheduled_tasks.schedule_tasks import send_leader_board_updates

load_dotenv()

initialise_database

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)


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
    return BoardOfShameRequest().handle()


@app.route('/post-config', methods=['POST'])
def post_config():
    return PostConfigRequest().handle()

@app.route('/toggle-perkele-pause', methods=['POST'])
def post_config():
    return TogglePerkelePauseRequest().handle()


@app.route('/health-check', methods=['GET'])
def health_check():
    return "I'm here", 200


@app.route('/run-perkele-check', methods=['POST'])
def run_perkele_check():
    PerkeleChecker().run()
    return "tasks run", 200


@app.route('/post-shame-boards', methods=['POST'])
def post_shame_boards():
    send_leader_board_updates()
    return "tasks run", 200


if __name__ == "__main__":
    app.run(debug=False)
