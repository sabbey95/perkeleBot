from flask import Response

from database import PerkeleCount
from requests.slash_command_request import SlashCommandRequest


class BoardOfShameRequest(SlashCommandRequest):
    def __init__(self, client):
        self.client = client
        super().__init__()

    def handle_channel(self, channel):
        send_board_of_shame(self.client, channel, self.session)
        return Response(), 200


def send_board_of_shame(client, channel, session):
    perkele_counts = session.query(PerkeleCount).filter(PerkeleCount.channel_id == channel.id).all()
    perkele_counts.sort(key=lambda x: x.perkele_count, reverse=True)
    heading_1 = " Offender     "
    heading_2 = " Offences "
    heading_section = "``` Perkele Board of Shame \n ---------------------------- \n" + heading_1 + heading_2 + "\n ========================= \n"
    middle_sections = map(lambda x: " <@" + x.user_id + ">   " + str(x.perkele_count) + "    ",
                          perkele_counts)
    table_section = '\n'.join(middle_sections)
    footer_section = "\n ------------------------- ```"
    client.chat_postMessage(channel=channel.id, text=(heading_section + table_section + footer_section))
