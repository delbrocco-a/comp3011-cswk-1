"""User Class"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class User(Base):
  __tablename__ = "users"

  id            = Column(Integer, primary_key=True, index=True)
  username      = Column(String, unique=True, nullable=False, index=True)
  email         = Column(String, unique=True, nullable=False, index=True)
  password_hash = Column(String, nullable=False)
  is_active     = Column(Boolean, default=True)
  created_at    = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  accounts   = relationship("Account", back_populates="user")
  categories = relationship("Category", back_populates="user")
  budgets    = relationship("Budget", back_populates="user")