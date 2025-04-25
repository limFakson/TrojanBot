import os
from .user_model import Base, User
from .transactions_model import Transaction
from sqlalchemy import create_engine, sessionmaker
import logging

logger = logging.getLogger(__name__)

#  Get DB config from env or default
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_NAME = os.getenv("DB_NAME", "wallet_bot.db")

# Create DB URL
if DB_TYPE == "postgres":
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = f"sqlite:///{DB_NAME}"

# Setup DB engine and session
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create tables
def init_db():
    logger.info(f"Connecting to database: {DATABASE_URL}")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully.")
