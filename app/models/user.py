from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base  # Import Base from models/__init__.py
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    events = relationship('Event', back_populates='owner')
    reviews = relationship('Reviews', back_populates='user')  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
        }

    def __repr__(self):
        return "User {}: {}".format(self.user_id, self.username)
