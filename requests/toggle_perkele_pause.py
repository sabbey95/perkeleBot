import datetime

from flask import Response

from database import Channel, TurnNotification
from requests.slash_command_request import SlashCommandRequest


class TogglePerkelePauseRequest(SlashCommandRequest):
    def handle_channel(self, channel):
        new_pause_status = not channel.paused
        self.session.query(Channel).filter(Channel.id == channel.id).update(
            {"paused": new_pause_status})
        self.session.query(TurnNotification).filter(TurnNotification.channel_id == channel.id).update(
                {'timestamp': datetime.datetime.now()})
        pause_info = "paused" if new_pause_status else "unpaused"
        self.client.chat_postMessage(channel=channel.id,
                                     text=f"This channel is now {pause_info} for Perkeles")

        return Response(), 200
