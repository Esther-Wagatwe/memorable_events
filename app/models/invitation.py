from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Invitation(Base):
    __tablename__ = 'Invitation'

    invitation_id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(45), nullable=False, default='Pending')
    guest_id = Column(Integer, ForeignKey('Guest.guest_id'), nullable=False)
    event_id = Column(Integer, ForeignKey('Event.event_id'), nullable=False)

    guest = relationship('Guest', back_populates='invitations')
    event = relationship('Event', back_populates='invitations')

    def serialize(self):
        return {
            'invitation_id': self.invitation_id,
            'status': self.status,
            'guest_id': self.guest_id,
            'event_id': self.event_id
        }

    def __repr__(self):
        return "Invitation {}: {}".format(self.invitation_id, self.status)
