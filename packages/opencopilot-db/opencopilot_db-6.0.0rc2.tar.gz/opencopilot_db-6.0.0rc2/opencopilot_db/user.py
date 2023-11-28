import uuid
from opencopilot_db.database_setup import Base, engine
from sqlalchemy import Column, String, DateTime
import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255))
    token = Column(String(255), nullable=True)
    email = Column(String(255), unique=True)
    email_verified_at = Column(DateTime, nullable=True)
    password = Column(String(255))
    remember_token = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


Base.metadata.create_all(engine)
