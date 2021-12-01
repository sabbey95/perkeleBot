from flask import Response

from database import PerkeleCount
from manual_config import SHAME_BOARD_TITLE
from requests.slash_command_request import SlashCommandRequest

COLUMN_START_PADDING = 1
COLUMN_END_PADDING = 4


class BoardOfShameRequest(SlashCommandRequest):
    def handle_channel(self, channel):
        send_board_of_shame(self.client, channel.id, self.session)
        return Response(), 200


def send_board_of_shame(client, channel_id, session):
    perkele_counts = session.query(PerkeleCount).filter(PerkeleCount.channel_id == channel_id).all()
    perkele_counts.sort(key=lambda x: x.perkele_count, reverse=True)
    users_list = client.users_list().get("members")
    board_of_shame = build_board_of_shame(perkele_counts, users_list)
    client.chat_postMessage(channel=channel_id, text=board_of_shame)


def build_board_of_shame(perkele_counts, users_list):
    heading_1 = "Offender"
    heading_2 = "Offences"

    column_1_width = get_row_width(heading_1, perkele_counts, users_list)
    column_2_width = len(heading_2) + COLUMN_START_PADDING + COLUMN_END_PADDING
    header_row = "%s%s" % (pad(heading_1, column_1_width), pad(heading_2, column_2_width))
    full_column_width = len(header_row)
    divider = "-" * full_column_width
    bold_divider = "=" * full_column_width
    heading_section = "```%s\n%s\n%s\n%s\n" % (
        pad(SHAME_BOARD_TITLE, full_column_width), divider, header_row, bold_divider)
    middle_sections = map(lambda x: build_shame_row(x, users_list),
                          perkele_counts)
    table_section = '\n'.join(middle_sections)
    footer_section = "\n%s```" % divider
    return heading_section + table_section + footer_section


def build_shame_row(perkele_count, users_list, column_1_width, column_2_width):
    user_id = perkele_count.user_id
    user_name = get_user_name(user_id, users_list)
    return "%s%s" % (pad(user_name, column_1_width), pad(str(perkele_count.perkele_count), column_2_width))


def get_user_name(user_id, users_list):
    user_info = next((x for x in users_list if x.get('id') == user_id), None)
    if user_info is not None:
        user_name = user_info.get('real_name') or user_info.get('name')
    else:
        user_name = "<@%s>" % user_id
    return user_name


def get_row_width(heading, perkele_counts, users_list):
    shameful_user_names = list(map(lambda x: get_user_name(x.id, users_list), perkele_counts))
    shameful_user_names.append(heading)
    return max(shameful_user_names, key=len) + COLUMN_END_PADDING + COLUMN_START_PADDING


def pad(string, length):
    spaces_at_end = length - COLUMN_START_PADDING - len(string)
    return '%s%s%s' % ('' * COLUMN_START_PADDING, string, ' ' * spaces_at_end)
