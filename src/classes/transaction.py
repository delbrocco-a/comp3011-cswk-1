"""Transaction Class"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Transaction(Base):
  __tablename__ = "transactions"

  id          = Column(Integer, primary_key=True, index=True)
  user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
  account_id  = Column(Integer, ForeignKey("accounts.id"), nullable=False)
  category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
  amount      = Column(Float, nullable=False)
  date        = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  description = Column(String)

  user     = relationship("User", back_populates="transactions")
  account  = relationship("Account", back_populates="transactions")
  category = relationship("Category", back_populates="transactions")