from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ 

password = environ.get("POSTGRES_PASSWORD")
user = environ.get("POSTGRES_USER")
db = environ.get("POSTGRES_DB")
dbhost = environ.get("dbhost")
SQLALCHEMY_DATABASE_URL = 'postgresql://{user}:{password}@{dbhost}:5432/{db}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

