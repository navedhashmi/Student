from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from config import get_settings

# Instance of Enviorment Variables
settings = get_settings()

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

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