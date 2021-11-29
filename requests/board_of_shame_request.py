from flask import Response

from database import PerkeleCount
from manual_config import SHAME_BOARD_TITLE
from requests.slash_command_request import SlashCommandRequest


class BoardOfShameRequest(SlashCommandRequest):
    def handle_channel(self, channel):
        send_board_of_shame(self.client, channel.id, self.session)
        return Response(), 200


def send_board_of_shame(client, channel_id, session):
    perkele_counts = session.query(PerkeleCount).filter(PerkeleCount.channel_id == channel_id).all()
    perkele_counts.sort(key=lambda x: x.perkele_count, reverse=True)
    board_of_shame = build_board_of_shame(perkele_counts, client)
    client.chat_postMessage(channel=channel_id, text=board_of_shame)


def build_board_of_shame(perkele_counts, client):
    heading_1 = "Offender"
    heading_2 = "Offences"
    divider = "----------------------------"
    heading_section = "``` %s \n %s \n %s       %s \n ========================= \n" % (
        SHAME_BOARD_TITLE, divider, heading_1, heading_2)
    middle_sections = map(lambda x: build_shame_row(x, client),
                          perkele_counts)
    table_section = '\n'.join(middle_sections)
    footer_section = "\n %s ```" % divider
    return heading_section + table_section + footer_section


def build_shame_row(perkele_count, client):
    user_id = perkele_count.user_id
    user_info = client.users_info(user_id)
    if user_info.get('ok'):
        user_name = user_info.get('user').get('name')
    else:
        user_name = "<@%s>" % user_id
    return "%s     %i    " % (user_name, perkele_count.perkele_count)
