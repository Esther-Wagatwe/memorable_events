from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func, select, case, Float
from sqlalchemy.ext.hybrid import hybrid_property
from . import Base
from .associations import event_vendor



class Vendor(Base):
    __tablename__ = 'Vendor'

    vendor_id = Column(Integer, primary_key=True, autoincrement=True)
    # event_id = Column(Integer, ForeignKey('Event.event_id'), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(45), nullable=True)
    description = Column(Text, nullable=True)
    image_path = Column(String(512), nullable=False)
    # cover_image = Column(String(512), nullable=True)
    # location = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    service_fee = Column(Integer, nullable=True)

    # event = relationship('Event', back_populates='vendors')
    reviews = relationship('Reviews', back_populates='vendor')
    events = relationship('Event', secondary=event_vendor, back_populates='vendors')

    def serialize(self):
        return {
            'vendor_id': self.vendor_id,
            # 'event_id': self.event_id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'image_path': self.image_path,
            'phone_number': self.phone_number,
            'email': self.email
        }

    def __repr__(self):
        return "Vendor {}: {}".format(self.vendor_id, self.name)

    @hybrid_property
    def average_review_score(self):
        score = 0
        for review in self.reviews:
            score += review.rating

        if len(self.reviews) > 0:
            return float(score / len(self.reviews))
        else:
            return 0
    
    @hybrid_property
    def review_score_str(self):
        return f"{self.average_review_score:.2f}"
    

    @hybrid_property
    def review_count(self):
        return len(self.reviews)
    
    
    @hybrid_property
    def review_starts(self):
        stars = int(self.average_review_score)
        return "★" * stars + "☆" * (5 - stars)
        
    
    @hybrid_property
    def clean_description(self):
        return str(self.description).strip().title() if self.description else "--empty--"
    
    
    
    