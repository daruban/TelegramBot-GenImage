from sqlalchemy import Column, Integer, Boolean, DateTime, JSON
from typing import Dict
from datetime import datetime
from TelegramBotGenImage.models.Base import Base, session
import json  

with open("TelegramBotGenImage/resource/body.json", "r", encoding="utf-8") as f:  
    body = json.load(f)  


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True, nullable=False, index=True)
    chat_data = Column(JSON, nullable=False, default=body)
    is_active = Column(Boolean, default=False) 
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, default=None)

    @classmethod
    def create(self, **kwargs):
        chat = self(
            chat_id = kwargs.get('chat_id'),
            chat_data = kwargs.get('body', body),
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
        chat = Chat.get(chat_id)
        if not chat:
            raise ValueError(f"Chat with chat_id {chat_id} not found")

        chat.chat_data = chat_data
        chat.updated_at = datetime.now()
        session.commit()
            
    @classmethod
    def soft_delete(cls, chat_id: int) -> None:
        """
        Мягкое удаление чата
        """
        chat = Chat.get(chat_id)
        
        if not chat:
            raise ValueError(f"Chat with chat_id {chat_id} not found")
            
        chat.is_active = False
        chat.deleted_at = datetime.now()
        session.commit()

    def __repr__(self):
        return f"<Chat(id={self.id}, chat_id={self.chat_id}, is_active={self.is_active})>"