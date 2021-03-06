from models.db import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Post(db.Model):
    __tablename__ = 'post'

# Column(s)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    review = db.Column(db.Integer, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'user.id', ondelete='cascade'), nullable=False)
    shelter_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'shelter.id', ondelete='cascade'), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False,
        onupdate=datetime.utcnow)

# Relationship(s)
    images = db.relationship(
        'Image', cascade='all',
        backref=db.backref('post', lazy="joined", innerjoin=True))
    comments = db.relationship(
        'Comment', cascade='all',
        backref=db.backref('post', lazy=True))

# Declarative Method(s)
    def __init__(self, body, title, review, user_id, shelter_id):
        self.body = body
        self.title = title
        self.review = review
        self.user_id = user_id
        self.shelter_id = shelter_id

    def json(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'body': self.body,
            'review': self.review,
            'user_id': str(self.user_id),
            "shelter_id": str(self.shelter_id),
            "images": [image.json()["id"] for image in self.images],
            "comments": [comment.json()["id"] for comment in self.comments],
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

# Class Method(s)
    @classmethod
    def find_all(cls):
        posts = Post.query.all()
        return posts

    @classmethod
    def by_id(cls, id):
        post = Post.query.filter_by(id=id).first()
        return post

    @classmethod
    def by_shelter(cls, shelter_id):
        posts = Post.query.filter_by(shelter_id=shelter_id).all()
        return posts

    def by_user(cls, user_id):
        posts = Post.query.filter_by(user_id=user_id).all()
        return posts
