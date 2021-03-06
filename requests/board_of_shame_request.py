import datetime
from functools import reduce
from itertools import groupby

from flask import Response

from database import PerkeleCount, Perkele
from manual_config import SHAME_BOARD_TITLE
from requests.slash_command_request import SlashCommandRequest

COLUMN_START_PADDING = 1
COLUMN_END_PADDING = 4


class BoardOfShameRequest(SlashCommandRequest):
    def handle_channel(self, channel):
        send_board_of_shame(self.client, channel.id, self.session)
        return Response(), 200


def send_board_of_shame(client, channel_id, session, all_time=True):
    perkele_counts = get_perkele_counts(channel_id, session, all_time)
    perkele_counts.sort(key=lambda x: x.perkele_count, reverse=True)
    users_list = client.users_list().get("members")
    board_of_shame = build_board_of_shame(perkele_counts, users_list, all_time)
    client.chat_postMessage(channel=channel_id, text=board_of_shame)


def get_perkele_counts(channel_id, session, all_time):
    perkeles = session.query(Perkele).filter(Perkele.channel_id == channel_id).all()
    if not all_time:
        current_date = datetime.datetime.now()
        perkeles = [p for p in perkeles if (current_date - p.timestamp).days <= 7]
    return group_perkeles(perkeles)


def group_perkeles(perkeles):
    return [make_perkele_count(key, group) for key, group in reduce(merge_dictionaries, perkeles, {}).items()]


def merge_dictionaries(acc, item):
    acc[item.user_id] = acc.get(item.user_id, 0) + 1
    return acc


def make_perkele_count(user_id, count):
    return PerkeleCount(id=user_id, channel_id=user_id, user_id=user_id,
                        perkele_count=count)


def build_board_of_shame(perkele_counts, users_list, all_time):
    heading_1 = "Offender"
    heading_2 = "Offences"

    column_1_width = get_row_width(heading_1, perkele_counts, users_list)
    header_row = "%s%s%s" % (pad(heading_1, column_1_width), heading_2, ' ' * COLUMN_END_PADDING)
    full_column_width = len(header_row)
    divider = "-" * full_column_width
    bold_divider = "=" * full_column_width
    heading_section = "```%s\n%s\n%s\n%s\n" % (
        pad(get_title(all_time), full_column_width), divider, header_row, bold_divider)
    middle_sections = map(lambda x: build_shame_row(x, users_list, column_1_width),
                          perkele_counts)
    table_section = '\n'.join(middle_sections)
    footer_section = "\n%s```" % divider
    return heading_section + table_section + footer_section


def get_title(all_time):
    timing_desc = 'All-time' if all_time else 'Weekly'
    return f'{timing_desc} {SHAME_BOARD_TITLE}'


def build_shame_row(perkele_count, users_list, column_1_width):
    user_id = perkele_count.user_id
    user_name = get_user_name(user_id, users_list)
    return "%s%i" % (pad(user_name, column_1_width), perkele_count.perkele_count)


def get_user_name(user_id, users_list):
    user_info = next((x for x in users_list if x.get('id') == user_id), None)
    if user_info is not None:
        user_name = user_info.get('real_name') or user_info.get('name')
    else:
        user_name = "<@%s>" % user_id
    return user_name


def get_row_width(heading, perkele_counts, users_list):
    shameful_user_names = list(map(lambda x: get_user_name(x.user_id, users_list), perkele_counts))
    shameful_user_names.append(heading)
    return len(max(shameful_user_names, key=len)) + COLUMN_END_PADDING + COLUMN_START_PADDING


def pad(string, length):
    spaces_at_end = length - COLUMN_START_PADDING - len(string)
    return '%s%s%s' % (' ' * COLUMN_START_PADDING, string, ' ' * spaces_at_end)
