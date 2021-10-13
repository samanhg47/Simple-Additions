from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from models.db import db
import uuid

from models.user import User


class Comment(db.Model):
    __tablename__ = 'comment'

# Column(s)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    body = db.Column(db.String(100), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'user.id', ondelete='cascade'), nullable=False)
    post_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'post.id', ondelete='cascade'), nullable=False)

# Declarative Method(s)
    def __init__(self, body, user_id, post_id):
        self.body = body
        self.user_id = user_id
        self.post_id = post_id

    def json(self):
        user_name = User.by_id(self.user_id).json()["user_name"]
        return {
            'id': str(self.id),
            "body": self.body,
            'user_id': str(self.user_id),
            "user_name": user_name,
            'post_id': str(self.post_id),
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
        return Comment.query.all()

    @classmethod
    def by_id(cls, id):
        id = UUID(id)
        return Comment.query.filter_by(id=id).first()

    @classmethod
    def by_user(cls, user_id):
        user_id = UUID(user_id)
        return Comment.query.filter_by(user_id=user_id).all()

    @classmethod
    def by_post(cls, post_id):
        post_id = UUID(post_id)
        return Comment.query.filter_by(post_id=post_id).all()
