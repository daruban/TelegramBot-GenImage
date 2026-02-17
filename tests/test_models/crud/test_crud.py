import pytest
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

from TelegramBotGenImage.models.Chat import Chat

class TestChatModel:
    """Тесты для модели Chat"""
    
    def test_create_chat_success(self, override_session, sample_chat_data):
        """Тест успешного создания чата"""
        chat = Chat.create(
            chat_id=12345,
            body=sample_chat_data
        )
        
        assert chat.id is not None
        assert chat.chat_id == 12345
        assert chat.chat_data == sample_chat_data
        assert chat.is_active is True
        assert chat.deleted_at is None
        
        saved_chat = override_session.query(Chat).filter_by(chat_id=12345).first()
        assert saved_chat is not None
        assert saved_chat.chat_data == sample_chat_data
    
    def test_create_chat_duplicate_fails(self, override_session, test_chat, sample_chat_data):
        """Тест создания чата с существующим chat_id"""
        with pytest.raises(IntegrityError):
            Chat.create(
                chat_id=12345,
                body={"other": "data"}
            )
    
    def test_get_existing_chat(self, override_session, test_chat):
        """Тест получения существующего чата"""
        found_chat = Chat.get(12345)
        
        assert found_chat is not None
        assert found_chat.id == test_chat.id
        assert found_chat.chat_data == test_chat.chat_data
        assert found_chat.is_active is True
    
    def test_get_nonexistent_chat(self, override_session):
        """Тест получения несуществующего чата"""
        found_chat = Chat.get(99999)
        
        assert found_chat is None
    
    def test_get_chat_with_different_id(self, override_session, test_chat, sample_chat_data):
        """Тест, что разные chat_id не путаются"""
        other_chat = Chat.create(
            chat_id=54321,
            body={"other": "chat"}
        )
        
        found_first = Chat.get(12345)
        found_second = Chat.get(54321)
        
        assert found_first.chat_data == sample_chat_data
        assert found_second.chat_data == {"other": "chat"}
    
    def test_update_chat_data(self, override_session, test_chat):
        """Тест обновления данных чата"""
        new_data = {
            "user": "updated_user",
            "messages": ["new_message"],
            "settings": {"language": "en"}
        }
        
        Chat.update_chat_data(12345, new_data)
        
        updated_chat = override_session.query(Chat).filter_by(chat_id=12345).first()
        assert updated_chat.chat_data == new_data
        assert updated_chat.updated_at > test_chat.created_at
    
    def test_update_nonexistent_chat(self, override_session):
        """Тест обновления несуществующего чата"""
        with pytest.raises(ValueError, match="Chat with chat_id 99999 not found"):
            Chat.update_chat_data(99999, {"data": "value"})
    
    def test_soft_delete_chat(self, override_session, test_chat):
        """Тест мягкого удаления чата"""
        Chat.soft_delete(12345)
        
        found_chat = Chat.get(12345)
        assert found_chat is None
        
        deleted_chat = override_session.query(Chat).filter_by(chat_id=12345).first()
        assert deleted_chat.is_active is False
        assert deleted_chat.deleted_at is not None
        assert isinstance(deleted_chat.deleted_at, datetime)
    
    def test_soft_delete_inactive_chat(self, override_session, test_chat):
        """Тест мягкого удаления уже неактивного чата"""
        test_chat.is_active = False
        override_session.commit()
        
        with pytest.raises(ValueError, match="Chat with chat_id 12345 not found"):
            Chat.soft_delete(12345)
    
    def test_get_only_active_chats(self, override_session, test_chat, sample_chat_data):
        """Тест, что get возвращает только активные чаты"""
        other_chat = Chat.create(
            chat_id=54321,
            body={"another": "chat"}
        )
        
        test_chat.is_active = False
        override_session.commit()
        
        assert Chat.get(12345) is None
        assert Chat.get(54321) is not None
    
    def test_get_ignores_deleted_chats(self, override_session, test_chat):
        """Тест, что get игнорирует мягко удаленные чаты"""

        test_chat.deleted_at = datetime.now()
        override_session.commit()
        
        assert Chat.get(12345) is None
    
    def test_multiple_chats_in_db(self, override_session, sample_chat_data):
        """Тест работы с несколькими чатами"""

        chat_ids = [1, 2, 3, 4, 5]
        for chat_id in chat_ids:
            Chat.create(
                chat_id=chat_id,
                body={"chat_id": chat_id, "data": sample_chat_data}
            )
        
        for chat_id in chat_ids:
            chat = Chat.get(chat_id)
            assert chat is not None
            assert chat.chat_data["chat_id"] == chat_id
    
    def test_chat_data_json_structure(self, override_session, test_chat):
        """Тест сохранения сложной JSON структуры"""
        complex_data = {
            "user": {
                "id": 1,
                "name": "John",
                "preferences": {
                    "theme": "dark",
                    "notifications": ["email", "sms"],
                    "last_seen": datetime.now().isoformat()
                }
            },
            "messages": [
                {"id": 1, "text": "Hello", "timestamp": "2024-01-01"},
                {"id": 2, "text": "World", "timestamp": "2024-01-02"}
            ],
            "metadata": {
                "created_from": "test",
                "version": "1.0.0"
            }
        }
        
        Chat.update_chat_data(12345, complex_data)
        
        updated_chat = Chat.get(12345)
        assert updated_chat.chat_data["user"]["preferences"]["theme"] == "dark"
        assert len(updated_chat.chat_data["messages"]) == 2
        assert updated_chat.chat_data["metadata"]["version"] == "1.0.0"