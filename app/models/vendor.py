from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Vendor(Base):
    __tablename__ = 'Vendor'

    vendor_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('Event.event_id'), nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(String(45), nullable=False)
    description = Column(Text, nullable=True)
    image_path = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)

    event = relationship('Event', back_populates='vendors')
    reviews = relationship('Reviews', back_populates='vendor')

    def serialize(self):
        return {
            'vendor_id': self.vendor_id,
            'event_id': self.event_id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'image_path': self.image_path,
            'phone_number': self.phone_number,
            'email': self.email
        }

    def __repr__(self):
        return "Vendor {}: {}".format(self.vendor_id, self.name)
