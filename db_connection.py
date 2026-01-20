# db_connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ORM import Base

DATABASE_URL = "postgresql+psycopg2://myuser:mypassword@localhost:5432/bom_simple"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

Session = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Create tables
Base.metadata.create_all(bind=engine)
