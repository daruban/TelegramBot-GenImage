import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from TelegramBotGenImage.models.Base import Base
from TelegramBotGenImage.models.Chat import Chat

@pytest.fixture(scope="function")
def db_session():
    """
    Временная бд SQLite в памяти для теста.
    """
    # Создаем engine для SQLite in-memory
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )
    
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(bind=engine)
    
    session = TestingSessionLocal()
    
    try:
        yield session 
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def override_session(db_session):
    """
    Подмена глобальной сессии на тестовую.
    """
    import TelegramBotGenImage.models.Chat
    
    # Сохраняем оригинальную сессию
    original_session = TelegramBotGenImage.models.Chat.session
    
    # Подменяем на тестовую
    TelegramBotGenImage.models.Chat.session = db_session
    
    yield db_session
    
    # Возвращаем оригинальные сессии
    TelegramBotGenImage.models.Chat.session = original_session

@pytest.fixture
def sample_chat_data():
    """
    Возвращает тестовые данные для чата
    """
    return {
        "user": "test_user",
        "messages": ["hello", "world"],
        "settings": {
            "language": "ru",
            "notifications": True
        }
    }

@pytest.fixture
def test_chat(override_session, sample_chat_data):
    """
    Создает тестовый чат в БД
    """
    from TelegramBotGenImage.models.Chat import Chat
    chat = Chat.create(
        chat_id = 12345,
        body = sample_chat_data
    )
    return chat

import pytest
from unittest.mock import Mock, MagicMock, patch
from telebot.types import Message, User, Chat

@pytest.fixture
def mock_telegram_user():
    """Мок пользователя Telegram"""
    user = Mock(spec=User)
    user.id = 12345
    user.first_name = "Test"
    user.last_name = "User"
    user.username = "testuser"
    return user

@pytest.fixture
def mock_telegram_chat():
    """Мок чата Telegram"""
    chat = Mock(spec=Chat)
    chat.id = 111666
    chat.type = "group"
    chat.title = "Test Group"
    return chat

@pytest.fixture
def mock_telegram_message(mock_telegram_user, mock_telegram_chat):
    """Мок сообщения Telegram"""
    message = Mock(spec=Message)
    message.message_id = 1
    message.from_user = mock_telegram_user
    message.chat = mock_telegram_chat
    message.date = 1116660
    message.text = "/start"
    message.json = {}
    return message

@pytest.fixture
def mock_bot():
    """Мок для bot объекта"""
    with patch('TelegramBotGenImage.bot') as mock:
        mock.send_message = MagicMock()
        mock.reply_to = MagicMock()
        yield mock

@pytest.fixture
def mock_telegram_message():
    """
    Фикстура для создания тестового сообщения Telegram
    """
    message = MagicMock()
    message.chat.id = 111666
    message.chat.type = "group"
    message.chat.title = "Test Group"
    message.from_user.id = 12345
    message.from_user.username = "tester"
    message.from_user.first_name = "Test"
    message.message_id = 1
    message.text = "/start"
    return message