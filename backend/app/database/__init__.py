import os
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from psycopg2 import OperationalError

SQLALCHEMY_DATABASE_URL = os.environ.get('POSTGRESQL_URI')

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
except OperationalError:
    import time
    time.sleep(5)
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
