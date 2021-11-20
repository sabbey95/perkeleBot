
from sqlalchemy.orm import sessionmaker
from database import get_database_engine


def new_database_session():
    session = sessionmaker(bind=get_database_engine())
    return session()
