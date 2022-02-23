from database import Channel, TurnNotification
from requests.board_of_shame_request import get_user_name
from requests.request import Request


class WhoseTurn(Request):
    def handle_session(self):
        turns = self.session.query(TurnNotification).all()
        strings = [make_turn_desc(t, self.client) for t in turns]
        return ' '.join(strings)


def make_turn_desc(turn, client):
    users_list = client.users_list().get("members")
    name = get_user_name(turn.user_id, users_list)
    channel = get_channel_name(turn.channel_id, client)
    return f"In {channel} it was {name}'s turn at {turn.timestamp.strftime('%H:%M:%S %d/%m/%Y')}."


def get_channel_name(channel_id, client):
    channel = client.conversations_info(channel=channel_id)
    if channel is not None:
        return channel.get('channel').get('name')
    else:
        return 'Unknown channel'
