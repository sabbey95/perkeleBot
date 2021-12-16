from flask import jsonify

from database import TurnNotification
from requests.request import Request


class ReplaceTurnNotification(Request):
    def __init__(self, name):
        self.name = name
        super().__init__()

    def handle_session(self):
        users_list = self.client.users_list().get("members")
        person = next((x for x in users_list if x.get('name').lower().__includes__(self.name.lower())), None)
        if person != None:
            self.session.query(TurnNotification).filter(
                TurnNotification.channel_id == 'C02HDGQ71NV').update(
                {'user_id': person.get('id')})
            return jsonify(person), 200
        return jsonify("Person: %s not found" % self.name), 200
