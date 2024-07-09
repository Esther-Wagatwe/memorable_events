from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.engine import Base

class Task(Base):
    __tablename__ = 'Task'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    status = Column(String(45), nullable=False)
    event_id = Column(Integer, ForeignKey('Event.event_id'), nullable=False)
    #due_date = Column(Date, nullable=False)

    event = relationship('Event', back_populates='tasks')

    def serialize(self):
        return {
            'task_id': self.task_id,
            'description': self.description,
            'status': self.status,
            #'due_date': self.due_date.isoformat() if self.due_date else None,
            'event_id': self.event_id
        }

    def __repr__(self):
        return f"Task {self.task_id}: {self.description}"
