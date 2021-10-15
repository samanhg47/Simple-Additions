import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from models.db import db
import uuid


class Shelter(db.Model):
    __tablename__ = 'shelter'

# Column(s)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shelter_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    latitude = db.Column(
        db.String(10), nullable=False)
    longitude = db.Column(
        db.String(10), nullable=False)
    password_digest = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

# Association(s)
    posts = db.relationship(
        "Post", cascade='all, delete', passive_deletes=True,
        backref=db.backref('shelter', lazy="joined", innerjoin=True))

# Declarative Method(s)
    def __init__(
            self, shelter_name, address, city, state, email, phone_number,
            latitude, longitude, password_digest):
        self.shelter_name = shelter_name
        self.address = address
        self.city = city
        self.state = state
        self.email = email
        self.phone_number = phone_number
        self.latitude = latitude
        self.longitude = longitude
        self.password_digest = password_digest

    def json(self):
        if self.address:
            address = "{}, {}, {}".format(self.address, self.city, self.state)
        else:
            address = "{}, {}".format(self.city, self.state)
        return {
            "id": str(self.id),
            "shelter_name": self.shelter_name,
            "address": address,
            "email": self.email,
            'phone_number': self.phone_number,
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "password_digest": self.password_digest,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "posts": self.posts
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

# Class Method(s)
    @classmethod
    def by_id(cls, id):
        return Shelter.query.filter_by(id=id).first()

    @classmethod
    def by_contacts(cls, phone_number, email, shelter_name, address):
        return Shelter.query.filter_by(phone_number=phone_number, email=email, shelter_name=shelter_name, address=address).first()

    @classmethod
    def find_all(cls):
        return Shelter.query.all()

    @classmethod
    def by_proximity(cls, coordinates, proximity):
        shelters = Shelter.find_all()
        all_shelters = [shelter.json() for shelter in shelters]
        # 68.93 miles/1 degree of latitude
        # 54.58 miles/1 degree of longitude
        # (latitude, longitude) ~ (x,y)
        if proximity:
            lat_r = proximity/68.93
            lon_r = proximity/54.58
            lat = coordinates["latitude"]
            lon = coordinates["longitude"]
            max_lat = lat + lat_r
            min_lat = lat - lat_r
            max_lon = lon + lon_r
            min_lon = lon - lon_r
            for index, shelter in enumerate(all_shelters):
                lat = shelter["latitude"]
                lon = shelter["longitude"]
                if lon > max_lon or lon < min_lon or lat > max_lat or lat < min_lat:
                    del all_shelters[index]
        return all_shelters
