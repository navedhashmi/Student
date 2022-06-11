from db_connection import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    isAdmin = Column(Boolean, server_default='FALSE', nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))
