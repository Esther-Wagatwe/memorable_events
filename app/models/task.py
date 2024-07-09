from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Task(Base):
    __tablename__ = 'Task'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    status = Column(String(45), nullable=False)
    event_id = Column(Integer, ForeignKey('Event.event_id'), nullable=False)

    event = relationship('Event', back_populates='tasks')

    def serialize(self):
        return {
            'task_id': self.task_id,
            'description': self.description,
            'status': self.status,
            'event_id': self.event_id
        }

    def __repr__(self):
        return "Task {}: {}".format(self.task_id, self.description)
