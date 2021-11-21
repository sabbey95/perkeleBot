from flask import Response

from manual_config import START_OF_CIV_DAY, END_OF_CIV_DAY
from requests.slash_command_request import SlashCommandRequest


class PostConfigRequest(SlashCommandRequest):
    def handle_channel(self, channel):
        start_time = START_OF_CIV_DAY.strftime("%H:%M")
        end_time = END_OF_CIV_DAY.strftime("%H:%M")
        config_string = "Perkeles are enabled in this channel:\n" \
                        "They will come after %i hours.\n" \
                        "Expected civ hours are from %s - %s on weekdays" % (
                            channel.hours_until_perkele, start_time,
                            end_time)
        self.client.chat_postMessage(channel=channel.id, text=config_string)
        return Response(), 200
