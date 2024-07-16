from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from . import Base
from .associations import event_vendor
import enum





class EventStatus(enum.Enum):
    ACTIVE = "active"
    DELETED = "deleted"
    ARCHIVED = "archived"
    UPCOMING = "upcoming"


class Event(Base):
    __tablename__ = 'Event'

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    
    location = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    date = Column(Date, nullable=False)
    name = Column(String(45), nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.ACTIVE)

    owner = relationship('User', back_populates='events')
    guests = relationship('Guest', back_populates='event')
    invitations = relationship('Invitation', back_populates='event')
    tasks = relationship('Task', back_populates='event')
    vendors = relationship('Vendor', secondary=event_vendor, back_populates='events')

    
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

    @hybrid_property
    def formatted_name(self):
        return str(self.name).strip().title()
    
    def get_event_name_str(self):
        return self.name
    
    @hybrid_property
    def formatted_date(self):
        return self.date.strftime("%B %d, %Y") if self.date else None
    
    @hybrid_property
    def guest_count(self):
        return len(self.guests)
    
    @hybrid_property
    def formatted_location(self):
        return str(self.location).strip().title()
    
    def get_event_total_cost(self):
        total_cost = 0
        for vendor in self.vendors:
            total_cost += vendor.service_fee
        return total_cost
    