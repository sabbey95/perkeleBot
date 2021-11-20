import datetime

import business_duration
import holidays

from database import Channel, TurnNotification, PerkeleCount
from database_utils import get_database_session


class PerkeleChecker:
    def __init__(self, client):
        self.session = get_database_session()
        self.client = client

    def run(self):
        channels = self.session.query(Channel).all()
        for channel in channels:
            self.__run_for_channel(channel)
        self.session.commit()

    def __run_for_channel(self, channel):
        last_notification = self.session.query(TurnNotification).filter(
            TurnNotification.channel_id == channel.id).first()
        if last_notification is not None and check_last_notification(last_notification, channel):
            user_id = last_notification.user_id
            self.client.chat_postMessage(channel=channel.id,
                                         text=("<@" + user_id + "> :perkele:"))
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


def check_last_notification(last_notification, channel):
    start_of_civ_day = datetime.time(8, 0, 0)
    end_of_civ_day = datetime.time(18, 0, 0)
    hours_dif = business_duration.businessDuration(last_notification.timestamp, datetime.datetime.now(),
                                                   starttime=start_of_civ_day, endtime=end_of_civ_day,
                                                   holidaylist=holidays.UnitedKingdom(), unit='hour', weekendlist=[])

    return hours_dif >= channel.hours_until_perkele
