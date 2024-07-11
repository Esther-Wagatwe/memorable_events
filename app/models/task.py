from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from . import Base

class Task(Base):
    __tablename__ = 'Task'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    status = Column(String(50), default='pending')
    event_id = Column(Integer, ForeignKey('Event.event_id'), nullable=False)
    due_date = Column(Date, nullable=False)

    event = relationship('Event', back_populates='tasks')

    def serialize(self):
        return {
            'task_id': self.task_id,
            'description': self.description,
            'status': self.status,
            'event_id': self.event_id,
            'due_date': self.due_date.isoformat()
        }

    def __repr__(self):
        return "Task {}: {}".format(self.task_id, self.description)
