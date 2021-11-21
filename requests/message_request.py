import datetime
import re

from database import TurnNotification
from requests.request import Request


class MessageRequest(Request):
    def __init__(self, event):
        self.event = event
        super().__init__()

    def get_channel_id(self):
        return self.event.get('channel')

    def handle_channel(self, channel):
        text = self.event.get('text')
        if channel.paused or text.__contains__('Perkele Board of Shame'):
            return

        mentions = re.findall('<@(.*?)>', text)
        if len(mentions) == 1:
            self.replace_current_notification(channel, mentions)

    def replace_current_notification(self, channel, mentions):
        turn_notification = TurnNotification(channel_id=channel.id,
                                             user_id=mentions[0], timestamp=datetime.datetime.now())
        self.session.query(TurnNotification).filter(TurnNotification.channel_id == channel.id).delete()
        self.session.add(turn_notification)
