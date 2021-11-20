from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_database_engine():
    return create_engine('sqlite:///database.db?check_same_thread=False', echo=False, )


def new_database_session():
    session = sessionmaker(bind=get_database_engine())
    return session()
