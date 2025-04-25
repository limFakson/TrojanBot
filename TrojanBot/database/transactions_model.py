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

# Base model
Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    token_address = Column(String, nullable=False)
    chain = Column(String, nullable=False)  # e.g., Ethereum, Solana
    tx_type = Column(String, nullable=False)  # buy, sell, swap, convert
    amount = Column(Float, nullable=False)
    token_symbol = Column(String, nullable=False)
    p_or_l_amount = Column(Float, nullable=True)
    status = Column(String, default="profit")
    tx_status = Column(String, default="pending")  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    wallet = relationship("Wallet", back_populates="transactions")
