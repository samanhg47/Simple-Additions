from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from models.db import db
from models.post import Post
from models.image import Image
from models.shelter import Shelter
from models.user import User
from models.comment import Comment
from resources import shelter, image, post, user, auth, comment


app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost:5432/flask_assocs"
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
migrate = Migrate(app, db)


api.add_resource(auth.UserLogin, 'login/users')
api.add_resource(auth.ShelterLogin, 'login/shelters')
api.add_resource(auth.UserRegister, 'register/users')
api.add_resource(auth.ShelterRegister, 'register/shelters')
api.add_resource(user.AllUsers, '/users')
api.add_resource(user.Users, '/user/<string:id>')
api.add_resource(comment.AllComments, '/comments')
api.add_resource(comment.Comments, '/comment/<string:id>')
api.add_resource(comment.PostComments, '/comments/<string:id>')
api.add_resource(comment.UserComments, 'user/comments/<string:id>')
api.add_resource(post.AllPosts, '/posts')
api.add_resource(post.Posts, '/post/<string:id>')
api.add_resource(post.ShelterPosts, '/posts/<string:id>')
api.add_resource(post.UserPosts, 'user/posts/<string:id>')
api.add_resource(image.AllImages, '/images')
api.add_resource(image.Images, '/image/<string:id>')
api.add_resource(image.PostImages, '/images/<string:id>')
api.add_resource(shelter.Allshelters, '/shelters')
api.add_resource(shelter.Allshelters, '/shelter/<string:id>')

if __name__ == '__main__':
    app.run(debug=True)
