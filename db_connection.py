from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from config import get_settings
import urllib, os

# Instance of Enviorment Variables
settings = get_settings()

ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}?sslmode={ssl_mode}"
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SeassionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Se = Session

# DB Connection|Session
def get_db():
    db = SeassionLocal()
    try:
        yield db
    finally:
        db.close()