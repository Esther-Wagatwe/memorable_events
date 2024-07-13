from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from . import Base
import enum

class EventStatus(enum.Enum):
    ACTIVE = "active"
    DELETED = "deleted"
    ARCHIVED = "archived"

class Event(Base):
    __tablename__ = 'Event'

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    date = Column(Date, nullable=False)
    name = Column(String(45), nullable=False)
    owner_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.ACTIVE)

    owner = relationship('User', back_populates='events')
    guests = relationship('Guest', back_populates='event')
    invitations = relationship('Invitation', back_populates='event')
    reviews = relationship('Reviews', back_populates='event')
    tasks = relationship('Task', back_populates='event')
    vendors = relationship('Vendor', back_populates='event')

    def serialize(self):
        return {
            'event_id': self.event_id,
            'location': self.location,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'name': self.name,
            'owner_id': self.owner_id
        }

    def __repr__(self):
        return "Event {}: {}".format(self.event_id, self.name)
