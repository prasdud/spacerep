from sqlalchemy import Column, String, DateTime
from .db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    priority = Column(String, default="moderate")
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    #description = Column(String, nullable=True) ---------> do we need this?
    