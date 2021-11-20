from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


def get_database_engine():
    url = os.environ['DATABASE_URL']
    return create_engine(url.replace("postgres://", "postgresql://", 1), echo=False, )


def new_database_session():
    session = sessionmaker(bind=get_database_engine())
    return session()
