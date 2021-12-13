from sqlalchemy import Column, Integer, String

from fastapi_database import Base

class Cities(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=True)
    timezone = Column(String, unique=False, index=True)
    time = Column(String, unique=False, index=True)