from flask import Response

from database import PerkeleCount
from requests.slash_command_request import SlashCommandRequest


class PostConfigRequest(SlashCommandRequest):
    def __init__(self, client):
        self.client = client
        super().__init__()

    def handle_channel(self, channel):
        config_string = "Perkeles are enabled in this channel:\n" \
                        "They will come after " + str(channel.hours_until_perkele) + " hours.\n" \
                        "Expected civ hours are from 8:00 - 18:00 on weekdays"
        client.chat_postMessage(channel=channel.id, text=config_string)
        return Response(), 200
