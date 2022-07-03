from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Column, DateTime, String


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    nick_name = Column(String(64), nullable=False)
    avatar_url = Column(String(128), nullable=False)
    type = Column(String(16), primary_key=True)
    created_time = Column(DateTime, nullable=False)
    modified_time = Column(DateTime, nullable=True)

