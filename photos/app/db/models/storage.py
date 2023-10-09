from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class Storage(Base):
    """Photo storage indexing model"""
    __tablename__ = 'storage'

    created_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    processed_date: Mapped[datetime] = mapped_column(nullable=True)
