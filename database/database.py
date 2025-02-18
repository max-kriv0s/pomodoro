from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import Settings

settings = Settings()
engine = create_engine('postgresql+psycopg2://postgres:password@0.0.0.0:5439/pomodoro')
Session = sessionmaker(engine)


def get_db_session():
    return Session