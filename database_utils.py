
from sqlalchemy.orm import sessionmaker
from database import get_database_engine

session = sessionmaker(bind=get_database_engine())
db_session = session()

def get_database_session():
    return db_session
