from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from TelegramBotGenImage.config.env import DB_URI

engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)

Base = declarative_base()
Base.metadata.create_all(engine)

session = Session()
