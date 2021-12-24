from database import Profanity
from flask import request

from requests.check_perkeles_request import get_profanity
from requests.request import Request


class AddProfanityRequest(Request):
    def handle_session(self):
        profanity = request.form.get('profanity')
        if not self.session.query(Profanity).filter(Profanity.profanity == profanity).first():
            self.session.add(Profanity(profanity=profanity))
            return "Thanks %s" % get_profanity(self.session), 200
        return "This profanity already exists, use your imagination", 200