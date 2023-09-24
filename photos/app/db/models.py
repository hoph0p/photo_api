import datetime

from sqlalchemy import Column, DateTime

from .base import Base


class Storage(Base):
    """Photo storage indexing model"""
    __tablename__ = 'storage'

    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    processed_date = Column(DateTime, nullable=True)
