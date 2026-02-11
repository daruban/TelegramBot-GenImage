from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.env import DB_URI

# Базовый класс для всех моделей
Base = declarative_base()

# Подключение к базе данных
engine = create_engine(DB_URI)

print("✅ Базовая настройка готова!")


# Создаем таблицу в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для работы с данными
Session = sessionmaker(bind=engine)
session = Session()

print("✅ Таблица создана, сессия готова!")
