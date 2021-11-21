from flask import Response

from database import PerkeleCount
from manual_config import SHAME_BOARD_TITLE
from requests.slash_command_request import SlashCommandRequest


class BoardOfShameRequest(SlashCommandRequest):
    def handle_channel(self, channel):
        send_board_of_shame(self.client, channel, self.session)
        return Response(), 200


def send_board_of_shame(client, channel, session):
    perkele_counts = session.query(PerkeleCount).filter(PerkeleCount.channel_id == channel.id).all()
    perkele_counts.sort(key=lambda x: x.perkele_count, reverse=True)
    board_of_shame = build_board_of_shame(perkele_counts)
    client.chat_postMessage(channel=channel.id, text=board_of_shame)


def build_board_of_shame(perkele_counts):
    heading_1 = "Offender"
    heading_2 = "Offences"
    divider = "----------------------------"
    heading_section = "``` %s \n %s \n %s       %s \n ========================= \n" % (
        SHAME_BOARD_TITLE, divider, heading_1, heading_2)
    middle_sections = map(lambda x: " <@%s>     %i    " % (x.user_id, x.perkele_count),
                          perkele_counts)
    table_section = '\n'.join(middle_sections)
    footer_section = "\n %s ```" % divider
    return heading_section + table_section + footer_section
