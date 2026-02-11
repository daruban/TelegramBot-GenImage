from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.env import DB_URI

Base = declarative_base()

engine = create_engine(DB_URI)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()




