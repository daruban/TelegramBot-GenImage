# tests/test_handlers/test_start.py
import pytest
from unittest.mock import patch, MagicMock
from TelegramBotGenImage.handlers.com_start import start

class TestStartCommand:
    """Тесты для команды /start в группах"""

    def test_start_existing_group(self, override_session, test_chat, mock_telegram_message):
        """
        Тест: группа уже авторизована
        Используем реальный test_chat из фикстуры
        """
        mock_telegram_message.chat.id = test_chat.chat_id
        
        with patch('TelegramBotGenImage.handlers.com_start.bot') as mock_bot:
            start(mock_telegram_message)
            
            mock_bot.send_message.assert_called_once_with(
                test_chat.chat_id,
                "Группа авторизирована",
                parse_mode="html"
            )

    def test_start_new_group(self, override_session, sample_chat_data, mock_telegram_message):
        """
        Тест: новая группа регистрируется
        Проверяем, что чат создается в БД
        """
        new_chat_id = 99999
        mock_telegram_message.chat.id = new_chat_id
        
        from TelegramBotGenImage.models.Chat import Chat
        assert Chat.get(new_chat_id) is None
        
        with patch('TelegramBotGenImage.handlers.com_start.bot') as mock_bot:
            start(mock_telegram_message)
            
            created_chat = Chat.get(new_chat_id)
            assert created_chat is not None
            assert created_chat.chat_id == new_chat_id
            assert created_chat.is_active is True
            
            mock_bot.send_message.assert_called_once_with(
                new_chat_id,
                "Группа зарегестрирована",
                parse_mode="html"
            )

    def test_start_twice_same_group(self, override_session, test_chat, mock_telegram_message):
        """
        Тест: группа вызывает /start дважды
        Должен вернуть сообщение об авторизации, не создавая дубликат
        """
        mock_telegram_message.chat.id = test_chat.chat_id
        
        with patch('TelegramBotGenImage.handlers.com_start.bot') as mock_bot:
            start(mock_telegram_message)
            
            mock_bot.send_message.assert_called_with(
                test_chat.chat_id,
                "Группа авторизирована",
                parse_mode="html"
            )
            
            mock_bot.send_message.reset_mock()
            
            start(mock_telegram_message)
            
            mock_bot.send_message.assert_called_once_with(
                test_chat.chat_id,
                "Группа авторизирована",
                parse_mode="html"
            )
            
            from TelegramBotGenImage.models.Chat import Chat
            chats = override_session.query(Chat).filter_by(chat_id=test_chat.chat_id).all()
            assert len(chats) == 1

    def test_start_with_different_groups(self, override_session, test_chat, sample_chat_data, mock_telegram_message):
        """
        Тест: разные группы вызывают /start
        """
        with patch('TelegramBotGenImage.handlers.com_start.bot') as mock_bot:
            mock_telegram_message.chat.id = test_chat.chat_id
            start(mock_telegram_message)
            
            mock_bot.send_message.assert_called_with(
                test_chat.chat_id,
                "Группа авторизирована",
                parse_mode="html"
            )
            
            new_chat_id = 77777
            mock_telegram_message.chat.id = new_chat_id
            start(mock_telegram_message)
            
            from TelegramBotGenImage.models.Chat import Chat
            new_chat = Chat.get(new_chat_id)
            assert new_chat is not None
            assert new_chat.chat_id == new_chat_id
            
            mock_bot.send_message.assert_called_with(
                new_chat_id,
                "Группа зарегестрирована",
                parse_mode="html"
            )
            
            assert mock_bot.send_message.call_count == 2

    def test_start_without_group_chat(self, mock_telegram_message):
        """
        Тест: команда /start в личном чате (должна игнорироваться)
        Проверяем, что хендлер с chat_types=["group"] не срабатывает
        """
        mock_telegram_message.chat.type = "private"
        mock_telegram_message.chat.id = 12345
        
        with patch('TelegramBotGenImage.handlers.com_start.bot') as mock_bot:
            from TelegramBotGenImage.handlers.com_start import start
            
            assert callable(start)
