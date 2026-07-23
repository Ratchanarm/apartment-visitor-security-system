from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Apartment(Base):
    __tablename__ = "apartments"

    id = Column(Integer, primary_key=True, index=True)
    building_name = Column(String(100), nullable=False)
    unit_number = Column(String(20), nullable=False)
    floor = Column(Integer)
    block = Column(String(20))
    address = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    residents = relationship("Resident", back_populates="apartment")
