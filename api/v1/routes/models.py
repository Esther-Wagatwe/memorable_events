from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(45), nullable=False)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }

    def __repr__(self):
        return "User {}: {}".format(self.user_id, self.username)

class Event(db.Model):
    __tablename__ = 'Event'

    event_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)

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
