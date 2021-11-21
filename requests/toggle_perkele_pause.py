from flask import jsonify

from database import Channel
from requests.slash_command_request import SlashCommandRequest


class TogglePerkelePauseRequest(SlashCommandRequest):
    def handle_channel(self, channel):
        new_pause_status = not channel.paused
        self.session.query(Channel).filter(Channel.id == channel.id).update(
            {"paused": new_pause_status})
        pause_info = "paused" if new_pause_status else "unpaused"
        return jsonify({"text": "This channel is now %s for Perkeles" % pause_info}), 200
