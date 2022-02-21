import os

from passlib.hash import sha256_crypt
from dotenv import load_dotenv
from flask import Flask, render_template
from slackeventsapi import SlackEventAdapter

import database as initialise_database
from flask import request

from auth import ENCRYPTED_MASTER_PASSWORD
from database_utils import get_database_session
from requests.add_profanity_request import AddProfanityRequest
from requests.board_of_shame_request import BoardOfShameRequest
from requests.check_perkeles_request import CheckPerkelesRequest
from requests.launch_bot_request import LaunchBotRequest
from requests.message_request import MessageRequest
from requests.post_config_request import PostConfigRequest
from requests.replace_notification_request import ReplaceTurnNotification
from requests.send_all_shame_boards_request import SendAllShameBoardsRequest
from requests.set_perkele_hours_request import SetPerkeleHoursRequest
from requests.toggle_perkele_pause import TogglePerkelePauseRequest

load_dotenv()

initialise_database

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

get_database_session().query(initialise_database.Perkele).all().delete()


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


@app.route('/replace-turn-notification', methods=['POST', 'GET'])
def replace_turn_notification():
    password = request.args.get('password')
    if not sha256_crypt.verify(password, ENCRYPTED_MASTER_PASSWORD):
        return "Who do you think you are?", 200
    name = request.args.get('name')
    return ReplaceTurnNotification(name).handle()


@app.route('/add-profanity', methods=['POST'])
def add_profanity():
    return AddProfanityRequest().handle()

@app.route('/', methods=['GET'])
def home_page():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=False)
