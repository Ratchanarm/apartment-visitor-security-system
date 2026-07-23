from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class SecurityGuard(Base):
    __tablename__ = "security_guards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_number = Column(String(50), unique=True)
    shift = Column(String(50))  # morning, evening, night
    assigned_gate = Column(String(50))
    is_on_duty = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
