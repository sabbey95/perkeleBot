from flask import Response, jsonify

from database import Channel
from manual_config import START_OF_CIV_DAY, END_OF_CIV_DAY, INACTIVE_ON_WEEKEND
from requests.slash_command_request import SlashCommandRequest


class TogglePerkelePauseRequest(SlashCommandRequest):
    def handle_channel(self, channel):
        self.session.query(Channel).filter(Channel.id == channel.id).update(
            {"paused": not channel.paused})
        text = "unpaused" if channel.paused else "paused"
        return jsonify({"text": "This channel is now %s for Perkeles" % text}), 200
