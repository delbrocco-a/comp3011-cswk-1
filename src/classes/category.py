"""Category Class"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Category(Base):
  __tablename__ = "categories"

  id          = Column(Integer, primary_key=True, index=True)
  user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
  name        = Column(String, nullable=False)
  description = Column(String)
  created_at  = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  user         = relationship("User", back_populates="categories")
  transactions = relationship("Transaction", back_populates="category")