from dotenv import load_dotenv
from sqlalchemy import String, Column, Integer, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

load_dotenv()
url = os.environ["DATABASE_URL"]
engine = create_engine(url.replace("postgres://", "postgresql://", 1), echo=False)


def get_database_engine():
    return engine


Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(String, primary_key=True)
    hours_until_perkele = Column(Integer)
    paused = Column(Boolean)


class TurnNotification(Base):
    __tablename__ = 'turn_notifications'

    channel_id = Column(String, primary_key=True)
    user_id = Column(String)
    timestamp = Column(DateTime)


class PerkeleCount(Base):
    __tablename__ = 'perkele_counts'

    id = Column(String, primary_key=True)
    channel_id = Column(String)
    user_id = Column(String)
    perkele_count = Column(Integer)


Base.metadata.create_all(get_database_engine(), checkfirst=True)


def find_channel(session, channel_id):
    return session.query(Channel).filter(Channel.id == channel_id).first()
