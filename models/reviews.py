from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from datetime import datetime

class Reviews(Base):
    __tablename__ = 'Reviews'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    review_date = Column(Date, nullable=False, default=datetime.now().date())
    vendor_id = Column(Integer, ForeignKey('Vendor.vendor_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)

    vendor = relationship('Vendor', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

    def serialize(self):
        return {
            'review_id': self.review_id,
            'rating': self.rating,
            'comment': self.comment,
            'review_date': self.review_date.isoformat() if self.review_date else None,
            'vendor_id': self.vendor_id,
            'event_id': self.event_id,
            'user_id': self.user_id
        }

    def __repr__(self):
        return "Review {}: {}".format(self.review_id, self.rating)
