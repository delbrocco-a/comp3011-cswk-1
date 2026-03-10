"""Budget Class"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Budget(Base):
  __tablename__ = "budgets"

  id          = Column(Integer, primary_key=True, index=True)
  user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
  category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
  amount      = Column(Float, nullable=False)
  start_date  = Column(DateTime, nullable=False)
  end_date    = Column(DateTime, nullable=False)
  created_at  = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  user     = relationship("User", back_populates="budgets")
  category = relationship("Category", back_populates="budgets")