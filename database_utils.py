from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


def get_database_engine():
    return create_engine(os.environ['DATABASE_URL'], echo=False, )


def new_database_session():
    session = sessionmaker(bind=get_database_engine())
    return session()
