import os
import logging
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Base model
Base = declarative_base()


# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    country = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    transactions = relationship("Transaction", back_populates="user")

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    wallet = Column(String, unique=True, index=True, nullable=True)
    wallet_address = Column(String, unique=True, nullable=False)
    preferred_chain = Column(String, nullable=True)  # e.g., Ethereum, Solana
    created_at = Column(DateTime, default=datetime.utcnow)

    user= relationship("User", back_populates="wallets")