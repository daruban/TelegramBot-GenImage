from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from datetime import datetime
from models import Base


# Модель = Python-класс = таблица в БД
class Chat(Base):
    __tablename__ = "chats"  # Имя таблицы
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True, nullable=False, index=True)
    chat_data = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
