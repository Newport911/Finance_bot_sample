from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from ..database import Base  # Исправляем на относительный импорт


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)