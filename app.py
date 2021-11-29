import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from slackeventsapi import SlackEventAdapter

import database as initialise_database
from requests.board_of_shame_request import BoardOfShameRequest
from requests.check_perkeles_request import CheckPerkelesRequest
from requests.launch_bot_request import LaunchBotRequest
from requests.message_request import MessageRequest
from requests.post_config_request import PostConfigRequest
from requests.request import Request
from requests.send_all_shame_boards_request import SendAllShameBoardsRequest
from requests.set_perkele_hours_request import SetPerkeleHoursRequest
from requests.toggle_perkele_pause import TogglePerkelePauseRequest

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
def toggle_perkele_pause():
    return TogglePerkelePauseRequest().handle()


@app.route('/health-check', methods=['GET'])
def health_check():
    return "I'm here", 200


@app.route('/run-perkele-check', methods=['POST', 'GET'])
def run_perkele_check():
    CheckPerkelesRequest().handle()
    return "tasks run", 200


@app.route('/post-shame-boards', methods=['POST', 'GET'])
def post_shame_boards():
    SendAllShameBoardsRequest().handle()
    return "tasks run", 200


@app.route('/replace-chris', methods=['POST', 'GET'])
def replace_chris():
    return ReplaceChris().handle()


class ReplaceChris(Request):
    def handle_session(self):
        users_list = self.client.users_list().get("members")
        people = map(lambda x: x.get('real_name'), users_list)
        return jsonify(people), 200


if __name__ == "__main__":
    app.run(debug=False)
