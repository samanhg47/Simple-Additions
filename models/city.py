from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from models.db import db
import uuid


class City(db.Model):
    __tablename__ = 'city'

# Column(s)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_name = db.Column(db.String(150), nullable=False)
    state_name = db.Column(db.String(25), nullable=False)
    state_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'state.id', ondelete='cascade'), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.DECIMAL(11, 6), nullable=False)
    longitude = db.Column(db.DECIMAL(11, 6), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

# Declarative Method(s)
    def __init__(self, city_name, state_name, state_id, zipcode, latitude, longitude):
        self.city_name = city_name
        self.state_name = state_name
        self.zipcode = zipcode
        self.state_id = state_id
        self.latitude = latitude
        self.longitude = longitude

    def json(self):
        return {
            "id": self.id,
            "city": self.city_name,
            "state": self.state_name,
            "zipcode": self.zipcode,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "state_id": self.state_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_all(cls):
        posts = City.query.all()
        return posts

    @classmethod
    def by_state(cls, state_name):
        posts = City.query.filter_by(state=state_name).all()
        return posts

    @classmethod
    def by_id(cls, city_id):
        post = City.query.filter_by(id=city_id).first()
        return post
