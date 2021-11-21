from flask import jsonify

from database import Channel
from requests.slash_command_request import SlashCommandRequest


class SetPerkeleHoursRequest(SlashCommandRequest):
    def handle_channel(self, channel):
        text = self.data.get('text')
        stripped_text = text.replace(' ', '')

        if stripped_text == '':
            return jsonify({"text": "Make sure to include the number of hours"}), 200

        if not stripped_text.isdigit():
            return jsonify({"text": "Make sure the number of hours is numeric"}), 200

        self.session.query(Channel).filter(Channel.id == channel.id).update(
            {"hours_until_perkele": int(stripped_text)})
        return jsonify({"text": "This channel now recieves Perkeles after %s hours" % stripped_text}), 200
