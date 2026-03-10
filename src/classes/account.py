"""Account Class"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Account(Base):
  __tablename__ = "accounts"

  id          = Column(Integer, primary_key=True, index=True)
  user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
  name        = Column(String, nullable=False)
  accountType = Column(String, nullable=False) 
  balance     = Column(Float, default=0.0)
  created_at  = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  user         = relationship("User", back_populates="accounts")
  transactions = relationship("Transaction", back_populates="account")