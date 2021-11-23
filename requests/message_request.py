import datetime
import re

from database import TurnNotification
from manual_config import SHAME_BOARD_TITLE
from requests.channel_request import ChannelRequest


class MessageRequest(ChannelRequest):
    def __init__(self, event):
        self.event = event
        super().__init__()

    def get_channel_id(self):
        return self.event.get('channel')

    def handle_channel(self, channel):
        text = self.event.get('text')
        if channel.paused or text.__contains__(SHAME_BOARD_TITLE):
            return

        mentions = re.findall('<@(.*?)>', text)
        if len(mentions) == 1:
            self.replace_current_notification(channel, mentions)

    def replace_current_notification(self, channel, mentions):
        turn_notification = TurnNotification(channel_id=channel.id,
                                             user_id=mentions[0], timestamp=datetime.datetime.now())
        self.session.query(TurnNotification).filter(TurnNotification.channel_id == channel.id).delete()
        self.session.add(turn_notification)
