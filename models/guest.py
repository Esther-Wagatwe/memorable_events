from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Guest(Base):
    __tablename__ = 'Guest'

    guest_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    status = Column(String(45), nullable=True)
    event_id = Column(Integer, ForeignKey('Event.event_id'), nullable=False)

    event = relationship('Event', back_populates='guests')
    invitations = relationship('Invitation', back_populates='guest')

    def serialize(self):
        return {
            'guest_id': self.guest_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'status': self.status,
            'event_id': self.event_id
        }

    def __repr__(self):
        return "Guest {}: {}".format(self.guest_id, self.name)
