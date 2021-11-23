from database import Channel
from requests.board_of_shame_request import send_board_of_shame
from requests.request import Request


class SendAllShameBoardsRequest(Request):
    def handle_session(self):
        channels = self.session.query(Channel).all()
        for channel in channels:
            send_board_of_shame(self.client, channel, self.session)