from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from models.db import db
import uuid


class State(db.Model):
    __tablename__ = 'state'

# Column(s)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state_name = db.Column(db.String(25), nullable=False)
    shorthand = db.Column(db.String(3), nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

# Association(s)
    cities = db.relationship(
        "City", cascade='all, delete', passive_deletes=True,
        backref=db.backref('state', lazy="joined", innerjoin=True))

# Declarative Method(s)
    def __init__(self, state_name, shorthand):
        self.state_name = state_name
        self.shorthand = shorthand

    def json(self):
        return {
            "id": str(self.id),
            "state_name": self.state_name,
            "shorthand": self.shorthand,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_all(cls):
        states = State.query.all()
        return states

    @classmethod
    def by_shorthand(cls, state_shorthand):
        state = State.query.filter_by(shorthand=state_shorthand).first()
        return state

    @classmethod
    def by_id(cls, id):
        id = uuid.UUID(id)
        state = State.query.filter_by(id=id).first()
        return state
