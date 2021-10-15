from resources import fileport, shelter, image, post, user, auth, comment, admin
from models.shelter import Shelter
from models.comment import Comment
from flask_migrate import Migrate
from models.image import Image
from dotenv import load_dotenv
from flask_restful import Api
from models.user import User
from models.post import Post
from flask_cors import CORS
from models.db import db
from flask import Flask
import os

load_dotenv()

UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY")

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost:5432/simple_additions_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_DIRECTORY'] = UPLOAD_DIRECTORY
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
migrate = Migrate(app, db)

# Auth Resource(s)
api.add_resource(auth.ShelterRegister, '/register/shelters')
api.add_resource(auth.ShelterLogin, '/login/shelters')
api.add_resource(auth.UserRegister, '/register/users')
api.add_resource(auth.UserLogin, '/login/users')

# Admin Resource(s)
api.add_resource(admin.AdminAllShelters, "/admin/shelters")
api.add_resource(admin.AdminAllComments, "/admin/comments")
api.add_resource(admin.AdminAllImages, "/admin/images")
api.add_resource(admin.AdminAllUsers, "/admin/users")
api.add_resource(admin.AdminAllPosts, "/admin/posts")

# User Resource(s)
api.add_resource(user.Users, '/user/<string:id>')
# api.add_resource(user.AllUsers, '/users')

# Comment Resource(s)
api.add_resource(comment.UserComments, '/user/comments/<string:id>')
# api.add_resource(comment.PostComments, '/comments/<string:id>')
api.add_resource(comment.Comments, '/comment/<string:id>')
api.add_resource(comment.AllComments, '/comments')

# Post Resource(s)
api.add_resource(post.UserPosts, '/user/posts/<string:id>')
# api.add_resource(post.ShelterPosts, '/posts/<string:id>')
api.add_resource(post.Posts, '/post/<string:id>')
api.add_resource(post.AllPosts, '/posts')

# Image Resource(s)
# api.add_resource(image.PostImages, '/images/<string:id>')
api.add_resource(image.Images, '/image/<string:id>')
api.add_resource(image.AllImages, '/images')

# File Resource(s)
api.add_resource(fileport.Uploads, "/upload")
api.add_resource(fileport.Downloads, "/download/<string:name>")

# Shelter Resource(s)
api.add_resource(shelter.Shelters, '/shelter/<string:id>')
api.add_resource(shelter.Allshelters, '/shelters')

if __name__ == '__main__':
    app.run(debug=True)
