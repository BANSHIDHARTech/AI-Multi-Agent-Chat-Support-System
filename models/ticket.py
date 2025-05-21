from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from database import Base

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum("open", "in_progress", "resolved", "closed", name="ticket_status"), default="open")
    priority = Column(Enum("low", "medium", "high", "urgent", name="ticket_priority"), default="medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Ticket(id={self.id}, subject='{self.subject}', status='{self.status}')>"
