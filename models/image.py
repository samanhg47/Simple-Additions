from models.db import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Image(db.Model):
    __tablename__ = 'image'

# Column(s)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    img_url = db.Column(db.String(250), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'user.id', ondelete='cascade'), nullable=False)
    post_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'post.id', ondelete='cascade'), nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False,
        onupdate=datetime.utcnow)

# Declarative Method(s)
    def __init__(self, img_url, post_id, user_id):
        self.img_url = img_url
        self.post_id = post_id
        self.user_id = user_id

    def json(self):
        return {'id': str(self.id), 'img_url': self.img_url, 'user_id': str(self.user_id), 'post_id': str(self.post_id),
                'created_at': str(self.created_at), 'updated_at': str(self.updated_at)}

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

# Class Method(s)
    @classmethod
    def find_all(cls):
        images = Image.query.all()
        return images

    @classmethod
    def by_id(cls, id):
        id = UUID(id)
        image = Image.query.filter_by(id=id).first()
        return image

    @classmethod
    def by_post(cls, post_id):
        post_id = UUID(post_id)
        posts = Image.query.filter_by(post_id=post_id).all()
        return posts
