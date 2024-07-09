from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base  # Import Base from models/__init__.py

class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    #role = Column(String(45), nullable=False)

    events = relationship('Event', back_populates='owner')
    reviews = relationship('Reviews', back_populates='user')  

    def serialize(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            #'role': self.role
        }

    def __repr__(self):
        return "User {}: {}".format(self.user_id, self.username)
