from database import Channel, TurnNotification
from requests.board_of_shame_request import get_user_name
from requests.request import Request


class WhoseTurn(Request):
    def handle_session(self):
        turns = self.session.query(TurnNotification).all()
        strings = [make_turn_desc(t, self.client) for t in turns]
        return '\n'.join(strings)


def make_turn_desc(turn, client):
    users_list = client.users_list().get("members")
    name = get_user_name(turn.user_id, users_list)
    channel = get_channel_name(turn.channel_id, client)
    return f"In {channel} it is {name}'s turn."


def get_channel_name(channel_id, client):
    channels = client.users_list().get("channels")
    print(channels)
    channel = next((x for x in channels if x.get('id') == channel_id), None)
    if channel is not None:
        return channel.get('name')
    else:
        return 'Unkown channel'
