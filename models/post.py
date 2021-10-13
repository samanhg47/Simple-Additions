from models.db import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Post(db.Model):
    __tablename__ = 'post'

# Column(s)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    review = db.Column(db.Integer, nullable=False)
    img_file_name = db.Column(db.string(100), nullable=False)
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
        'Image', cascade='all, delete', passive_deletes=True,
        backref=db.backref('post', lazy=True),)

# Declarative Method(s)
    def __init__(self, body, title, review, user_id, img_file_name, shelter_id):
        self.body = body
        self.title = title
        self.review = review
        self.user_id = user_id
        self.img_file_name = img_file_name
        self.shelter_id = shelter_id

    def json(self):
        return {'id': str(self.id), 'title': self.title, 'body': self.body,
                'review': self.review, 'user_id': str(self.user_id), "shelter_id": str(self.shelter_id),
                'created_at': str(self.created_at), 'updated_at': str(self.updated_at)}

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
    def by_id(cls, post_id):
        post = Post.query.filter_by(id=post_id).first()
        return post

    @classmethod
    def by_shelter(cls, shelter_id):
        posts = Post.query.filter_by(shelter_id=shelter_id).all()
        return posts

    def by_user(cls, user_id):
        posts = Post.query.filter_by(user_id=user_id).all()
        return posts
