from flask import Response

from manual_config import START_OF_CIV_DAY, END_OF_CIV_DAY, INACTIVE_ON_WEEKEND
from requests.slash_command_request import SlashCommandRequest


class PostConfigRequest(SlashCommandRequest):
    def handle_channel(self, channel):
        config_string = build_config(channel)
        self.client.chat_postMessage(channel=channel.id, text=config_string)
        return Response(), 200


def build_config(channel):
    start_time = START_OF_CIV_DAY.strftime("%H:%M")
    end_time = END_OF_CIV_DAY.strftime("%H:%M")
    day_info = "excluding weekends" if INACTIVE_ON_WEEKEND else ""
    config_string = "Perkeles are enabled in this channel:\n" \
                    "They will come after %i hours.\n" \
                    "Expected civ hours are from %s - %s %s" % (
                        channel.hours_until_perkele, start_time,
                        end_time, day_info)
    return config_string
