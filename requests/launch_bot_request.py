from flask import jsonify

from database import Channel
from requests.slash_command_request import SlashCommandRequest


class LaunchBotRequest(SlashCommandRequest):
    def handle_channel(self, channel):
        return jsonify({"text": "This channel is already subscribed"}), 200

    def handle_no_channel(self, channel_id):
        channel = Channel(id=channel_id, hours_until_perkele=5, paused=False)
        self.session.add(channel)
        return jsonify({"text": "This channel is now subscribed to Perkeles"}), 200
