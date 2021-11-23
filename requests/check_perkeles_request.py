import datetime

import business_duration
import holidays

from database import Channel, TurnNotification, PerkeleCount
from manual_config import START_OF_CIV_DAY, END_OF_CIV_DAY, INACTIVE_ON_WEEKEND
from requests.request import Request


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
            user_id = last_notification.user_id
            self.client.chat_postMessage(channel=channel.id,
                                         text=("<@%s> :perkele:" % user_id))
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
    hours_dif = business_duration.businessDuration(last_notification.timestamp, datetime.datetime.now(),
                                                   starttime=START_OF_CIV_DAY, endtime=END_OF_CIV_DAY,
                                                   holidaylist=holidays.UnitedKingdom(), unit='hour',
                                                   weekendlist=weekends)

    return hours_dif >= channel.hours_until_perkele
