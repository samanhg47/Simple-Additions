from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from models.db import db
import uuid


class User(db.Model):
    __tablename__ = 'user'

# Column(s)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = db.Column(db.String(50), nullable=False)
    password_digest = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    city_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'city.id', ondelete='cascade'), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

# Association(s)
    posts = db.relationship(
        "Post", cascade='all, delete', passive_deletes=True,
        backref=db.backref('user', lazy="joined", innerjoin=True))
    comments = db.relationship(
        "Comment", cascade='all, delete', passive_deletes=True,
        backref=db.backref('user', lazy="joined", innerjoin=True))
    images = db.relationship(
        "Image", cascade='all, delete', passive_deletes=True,
        backref=db.backref('user', lazy="joined", innerjoin=True))

# Declarative Method(s)
    def __init__(self, user_name, password_digest, email, city_id):
        self.user_name = user_name
        self.password_digest = password_digest
        self.email = email
        self.city_id = city_id

    def json(self):
        return {
            "id": str(self.id),
            "user_name": self.user_name,
            "email": self.email,
            "password_digest": self.password_digest,
            "city_id": str(self.city_id),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "posts": [post.json()["id"] for post in self.posts],
            "comments": [comment.json()["id"] for comment in self.comments]
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

# Class Method(s)
    @classmethod
    def find_all(cls):
        return User.query.all()

    @classmethod
    def by_id(cls, id):
        return User.query.filter_by(id=id).first()

    @classmethod
    def by_name(cls, name):
        return User.query.filter_by(user_name=name).first()
