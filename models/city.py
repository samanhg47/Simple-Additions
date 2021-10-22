from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from models.db import db
import uuid


class City(db.Model):
    __tablename__ = 'city'

# Column(s)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_name = db.Column(db.String(150), nullable=False)
    state_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'state.id', ondelete='cascade'), nullable=False)
    state_name = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.DECIMAL(11, 6), nullable=False)
    longitude = db.Column(db.DECIMAL(11, 6), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

# Association(s)
    users = db.relationship(
        "User", cascade='all, delete', passive_deletes=True,
        backref=db.backref('user', lazy="joined", innerjoin=True))

# Declarative Method(s)
    def __init__(self, city_name, state_id, zipcode, latitude, longitude, state_name):
        self.city_name = city_name
        self.zipcode = zipcode
        self.state_id = state_id
        self.latitude = latitude
        self.longitude = longitude
        self.state_name = state_name

    def json(self):
        users = []
        for user in self.users:
            user = user.json()["id"]
            users.append(user)
        return {
            "id": str(self.id),
            "city": self.city_name,
            "zipcode": self.zipcode,
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "state_name": self.state_name,
            "users": users,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_all(cls):
        cities = City.query.all()
        return cities

    @classmethod
    def by_state(cls, name):
        cities = City.query.filter_by(state_name=name).all()
        return cities

    @classmethod
    def by_id(cls, city_id):
        city = City.query.filter_by(id=city_id).first()
        return city

    @classmethod
    def by_info(cls, state, name, zip):
        city = City.query.filter_by(
            state_name=state, city_name=name, zipcode=zip).first()
        return city

    @classmethod
    def zipcodes(cls, state, name):
        cities = City.query.filter_by(
            state_name=state, city_name=name).all()
        return cities
