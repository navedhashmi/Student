from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:9887917957@localhost/student"

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