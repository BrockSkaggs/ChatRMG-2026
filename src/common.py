import datetime as dt
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional

base_ollama_url = "http://ollama:11434"

#PostgresSQL
DB_HOSTNAME = 'postgres'
DB_PORT = 5432
DB_NAME = 'dashGPT'
USER_NAME = 'postgres'
USER_PWD = 'password'

def gen_postgres_conn_str(for_sqlalchemy: Optional[bool] = True) -> str:
    if for_sqlalchemy:
        return f'postgresql+psycopg://{USER_NAME}:{USER_PWD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}' #Added driver for SQLAchemy engine creation
    return f'postgresql://{USER_NAME}:{USER_PWD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}' #Original

dashgpt_engine = create_engine(
    gen_postgres_conn_str(),
    pool_size=20,
    max_overflow=25
)

def create_alchemy_session(engine):
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()

def get_central_time(utc_time: dt.datetime) -> dt.datetime:
    return utc_time + dt.timedelta(hours=-6)