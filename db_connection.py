# db_connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ORM import Base

engine=create_engine("sqlite:///bom_simple.db")
Session=sessionmaker(bind=engine)
Base.metadata.create_all(engine)
