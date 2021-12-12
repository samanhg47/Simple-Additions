from sqlalchemy.dialects.postgresql import UUID
from models.state import State
from datetime import datetime
from models.city import City
from models.db import db
import uuid


class Shelter(db.Model):
    __tablename__ = 'shelter'
    __table_args__ = (
        db.UniqueConstraint('shelter_name', 'address', name="nameNaddress"),
    )

# Column(s)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shelter_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    city_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'city.id', ondelete='cascade'), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    latitude = db.Column(
        db.DECIMAL(11, 6), nullable=False)
    longitude = db.Column(
        db.DECIMAL(11, 6), nullable=False)
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
            self, shelter_name, address, city_id, email, phone_number,
            latitude, longitude, password_digest):
        self.shelter_name = shelter_name
        self.address = address
        self.city_id = city_id
        self.email = email
        self.phone_number = phone_number
        self.latitude = latitude
        self.longitude = longitude
        self.password_digest = password_digest

    def json(self):
        city = City.by_id(str(self.city_id)).json()
        return {
            "id": str(self.id),
            "shelter_name": self.shelter_name,
            "address": self.address,
            "email": self.email,
            'phone_number': self.phone_number,
            'state': city['state_name'],
            'city': city['city'],
            'zipcode': city['zipcode'],
            'city_id': str(self.city_id),
            "latitude": float(self.latitude),
            "longitude": float(self.longitude),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "posts": [post.json()["id"] for post in self.posts]
        }

    def password(self):
        return self.password_digest

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

# Class Method(s)
    @classmethod
    def by_id(cls, id):
        id = uuid.UUID(id)
        return Shelter.query.filter_by(id=id).first()

    @classmethod
    def by_address(cls, shelter_name, address):
        return Shelter.query.filter_by(shelter_name=shelter_name, address=address).first()

    @classmethod
    def find_all(cls):
        return Shelter.query.all()

    @classmethod
    def by_proximity(cls, coordinates, proximity):
        # 68.93 miles/1 degree of latitude
        # 54.58 miles/1 degree of longitude
        # (latitude, longitude) ~ (x,y)
        print()
        print()
        print(coordinates)
        print(proximity)
        print()
        print()
        if proximity > 0:
            shelters = [shelter.json() for shelter in Shelter.find_all()]
            lat_r = proximity/68.93
            lon_r = proximity/54.58
            lat = coordinates["lat"]
            lon = coordinates["lng"]

            max_lat = lat + lat_r
            min_lat = lat - lat_r
            max_lon = lon + lon_r
            min_lon = lon - lon_r
            for index, shelter in enumerate(shelters):
                lat = shelter["latitude"]
                lon = shelter["longitude"]
                if lon > max_lon or lon < min_lon or lat > max_lat or lat < min_lat:
                    del shelters[index]
            return shelters
        states = {state.json()['shorthand']: [] for state in State.find_all()}
        for shelter in Shelter.find_all():
            states[shelter.json()['state']].append(shelter.json())
        print()
        print()
        print("states")
        print(states['WY'])
        print()
        print()
        return states
