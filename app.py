import random

from flask.cli import with_appcontext
from middleware import gen_password
from resources import fileport, shelter, image, post, user, auth, comment, admin
from faker.providers.person.en import Provider
from faker.providers import internet
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
from faker import Faker
import click
import os
from random import shuffle, seed
from sheets import all_shelters
from flask.cli import AppGroup

load_dotenv()

UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY")

app = Flask(__name__)
CORS(app)
api = Api(app)
seed_cli = AppGroup("seed")


@seed_cli.command("users")
@click.option('--amount', default=20, help='number of users to be generated')
# @click.command('--create')
# @click.option('--create', default="none", help='number of users to be generated')
# @click.option('--amount', default=0, help='number of users to be generated')
# @click.option('--run', default=, help='number of users to be generated')
# @with_appcontext
def seeder(amount):
    if amount > 0:
        first_names = list(set(Provider.first_names))
        last_names = list(set(Provider.last_names))
        seed(4321)
        shuffle(first_names)
        shuffle(last_names)
        random_usernames = []
        random_emails = []

        click.echo('Working...')
        # Ensure we get the makeusers number of usernames.

        def name_check(rand_names, index):
            for username in random_usernames:
                if rand_names[index] in username or "'" in rand_names[index]:
                    index += 1
                    name_check(rand_names, index)
            return rand_names[index]

        def random_address():
            str = "123456789"
            address = ""
            num = random.choice(str[1:4])[0]
            for char in random.choices(str, k=int(num)):
                address += char
            return address

        for i in range(0, amount):
            random_usernames.insert(0, name_check(
                first_names, i)+"_"+name_check(last_names, i) + random_address())
        for name in random_usernames:
            random_emails.append(
                name + "@" + Faker().free_email_domain())
        while True:
            if len(random_usernames) == 0 or len(random_emails) == 0:
                break

            username = random_usernames.pop()
            password = gen_password("1234")
            email = random_emails.pop()
            user = User(username, password, email)
            db.session.add(user)
            db.session.commit()

    click.echo(
        '{} users were added to the database.'.format(amount,))


app.cli.add_command(seed_cli)
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
    # seeder()
    app.run(debug=True)
