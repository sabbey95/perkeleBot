import datetime

from flask import jsonify

from database import TurnNotification
from requests.request import Request


class ReplaceTurnNotification(Request):
    def __init__(self, name):
        self.name = name
        super().__init__()

    def handle_session(self):
        users_list = self.client.users_list().get("members")
        person = next((x for x in users_list if x.get('profile').get('display_name').__contains__(self.name)), None)
        if person is not None:
            self.session.query(TurnNotification).filter(
                TurnNotification.channel_id == 'C02HDGQ71NV').update(
                {'user_id': person.get('id'), 'timestamp': datetime.datetime.now()})
            return jsonify(person), 200
        return jsonify("Person: %s not found" % self.name), 200
