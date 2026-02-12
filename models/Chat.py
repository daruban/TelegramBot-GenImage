from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from typing import Optional, List, Type, TypeVar, Generic, Dict
from datetime import datetime
from models.Base import Base, session
import json  

with open("resource/body.json", "r", encoding="utf-8") as f:  
    body = json.load(f)  


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True, nullable=False, index=True)
    chat_data = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=False) 
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, default=None)

    @classmethod
    def create(self, **kwargs):
        chat = self(
            chat_id = kwargs.get('chat_id'),
            chat_data = body,
            is_active = True,
            created_at = datetime.now(),
            updated_at = datetime.now(),
        )
        session.add(chat)
        session.commit()
        return chat

    @classmethod
    def get(self, chat_id):
        return session.query(self).filter_by(chat_id = chat_id, is_active = True, deleted_at = None).first()

    @classmethod
    def update_chat_data(self, chat_id: int, chat_data: Dict):
        chat = session.query(self).filter_by(chat_id = chat_id, is_active = True, deleted_at = None).first()
        chat.chat_data = chat_data
        session.commit()