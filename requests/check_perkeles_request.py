import datetime
import random

import business_duration
from govuk_bank_holidays.bank_holidays import BankHolidays
from requests.request import Request

from database import Channel, TurnNotification, PerkeleCount, Profanity
from manual_config import START_OF_CIV_DAY, END_OF_CIV_DAY, INACTIVE_ON_WEEKEND

class CheckPerkelesRequest(Request):
    def handle_session(self):
        channels = self.session.query(Channel).all()
        for channel in channels:
            if not channel.paused:
                self.__run_for_channel(channel)

    def __run_for_channel(self, channel):
        last_notification = self.session.query(TurnNotification).filter(
            TurnNotification.channel_id == channel.id).first()
        if last_notification is not None and deserves_perkele(last_notification, channel):
            profanity = get_profanity(self.session)
            user_id = last_notification.user_id
            self.client.chat_postMessage(channel=channel.id,
                                         text=f"<@{user_id}> :perkele:  {profanity}")
            self.__update_perkele_count(user_id, channel.id)

    def __update_perkele_count(self, user_id, channel_id):
        filter = self.session.query(PerkeleCount).filter(PerkeleCount.user_id == user_id,
                                                         PerkeleCount.channel_id == channel_id)
        current_perkele_count = filter.first()
        if current_perkele_count is None:
            new_perkele_count = PerkeleCount(id=(channel_id + user_id), user_id=user_id, channel_id=channel_id,
                                             perkele_count=1)
            self.session.add(new_perkele_count)
        else:
            filter.update({'perkele_count': current_perkele_count.perkele_count + 1})


def deserves_perkele(last_notification, channel):
    weekends = [5, 6] if INACTIVE_ON_WEEKEND else []
    bank_holidays = BankHolidays(use_cached_holidays=True).get_holidays()
    mins_dif = business_duration.businessDuration(last_notification.timestamp, datetime.datetime.now(),
                                                   starttime=START_OF_CIV_DAY, endtime=END_OF_CIV_DAY,
                                                   holidaylist=bank_holidays, unit='min',
                                                   weekendlist=weekends)

    return mins_dif >= (channel.hours_until_perkele * 60)


def get_profanity(session):
    profanities = list(map(lambda x: x.profanity, session.query(Profanity).all()))
    random_limit = max(len(profanities), 20)
    index = random.randint(0, random_limit-1)
    if index >= len(profanities):
        return "Perkele"
    return profanities[index]

