from resources import fileport, shelter, image, post, user, auth, comment, admin
from random import shuffle, seed, choices, choice
from faker.providers.person.en import Provider
from middleware import gen_password
from models.shelter import Shelter
from models.comment import Comment
from flask_migrate import Migrate
from sheets import all_shelters
from models.image import Image
from flask.cli import AppGroup
from dotenv import load_dotenv
from flask_restful import Api
from models.user import User
from models.post import Post
from flask_cors import CORS
from models.db import db
from gevent import sleep
from flask import Flask
from faker import Faker
from dog import getDog
from uuid import UUID
import requests
import click
import boto3
import os

load_dotenv()
UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY")

app = Flask(__name__)
CORS(app)
api = Api(app)
seed_cli = AppGroup("seed")
burn_cli = AppGroup("burn")

S3_BUCKET = os.getenv("S3_BUCKET")
S3_USER_ID = os.getenv("S3_USER_ID")
S3_USER_SECRET = os.getenv("S3_USER_SECRET")
S3_REGION = os.getenv("S3_REGION")


# seed users
@seed_cli.command("users")
@click.option('--amount', default=20, help='number of users to be generated')
def user_seeder(amount):
    if amount > 0:
        first_names = list(set(Provider.first_names))
        last_names = list(set(Provider.last_names))
        seed(4321)
        shuffle(first_names)
        shuffle(last_names)
        random_usernames = []
        random_emails = []

        click.echo('seeding...')

        def name_check(rand_names, index):
            for username in random_usernames:
                if rand_names[index] in username or "'" in rand_names[index]:
                    index += 1
                    name_check(rand_names, index)
            return rand_names[index]

        def num_tail():
            str = "123456789"
            address = ""
            num = choice(str[1:4])[0]
            for char in choices(str, k=int(num)):
                address += char
            return address

        for i in range(0, amount):
            random_usernames.insert(0, name_check(
                first_names, i)+"_"+name_check(last_names, i) + num_tail())
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
            user.create()

    click.echo(
        '{} users were added to the database.'.format(amount,))


# burn users
@burn_cli.command("users")
@click.option("--amount", default="all", help='number of users to be deleted')
def user_destroyer(amount):
    users = [user for user in User.find_all()]
    if amount == "all":
        amount = len(users)
    else:
        amount = int(amount)
    count = 0
    if amount > 0:
        for _ in range(0, amount):
            db.session.delete(users[count])
            db.session.commit()
            count += 1
    click.echo("{} users where destroyed".format(count))


# seed shelters
@seed_cli.command("shelters")
@click.option('--amount', default="20", help='number of shelters to be generated')
def shelter_seeder(amount):
    if int(amount) > 0 or amount == "all":
        if amount == "all":
            amount = 10137
        else:
            amount = int(amount)
        click.echo('seeding...')

        shelter_list = []
        for shelter in all_shelters:
            if len(shelter_list) >= amount:
                break
            if not Shelter.by_contacts(shelter['phone_number'], shelter['email'], shelter['shelter_name'], shelter['address']):
                shelter_name = shelter['shelter_name']
                password_digest = gen_password(shelter['password'])
                email = shelter['email']
                address = shelter['address']
                state = shelter['state']
                city = shelter['city']
                phone_number = shelter['phone_number']
                latitude = shelter['latitude']
                longitude = shelter['longitude']
                this_model = Shelter(
                    shelter_name, address, city, state, email,
                    phone_number, latitude, longitude, password_digest
                )
                this_model.create()
                shelter_list.append(this_model)

    click.echo(
        '{} shelters were added to the database.'.format(amount))


# burn shelters
@burn_cli.command("shelters")
@click.option("--amount", default="all", help='number of shelters to be deleted')
def shelter_destroyer(amount):
    shelters = [shelter for shelter in Shelter.find_all()]
    if amount == "all":
        amount = len(shelters)
    else:
        amount = int(amount)
    count = 0
    if amount > 0:
        for _ in range(0, amount):
            db.session.delete(shelters[count])
            db.session.commit()
            count += 1
    click.echo("{} shelters where destroyed".format(count))


# seed posts
@seed_cli.command("posts")
def post_seeder():
    sleep(1)
    seed(4321)
    click.echo('seeding...')
    shelter_comi = [shelter.json() for shelter in Shelter.find_all()]
    img_count = 0
    post_count = 0
    users = User.find_all()
    users = [user.json() for user in users]
    shelters = [shelter.json() for shelter in Shelter.find_all()]
    post_arr = []
    for shelt in shelter_comi:
        if len(shelt["posts"]) == 0:

            number = choice(range(1, 5))
            post_arr = []
            while number > len(post_arr):
                shuffle(users)
                shuffle(shelters)
                length = choice(range(20, 50))
                body = ""
                while len(body.split(' ')) < length:
                    body = body + " " + Faker().catch_phrase() + "."
                    body = body + " " + Faker().bs().capitalize() + "."
                title = Faker().catch_phrase()
                review = choice(range(7, 10))
                params = {
                    "body": body,
                    "title": title,
                    "review": review,
                    "user_id": UUID(choice(users)["id"]),
                    "shelter_id": UUID(shelt["id"])
                }
                post = Post(**params)
                post.create()

                # post images
                img_list = []
                s3_user = boto3.client(
                    's3',
                    aws_access_key_id=S3_USER_ID,
                    aws_secret_access_key=S3_USER_SECRET,
                    region_name=S3_REGION
                )
                key_smith = "qwertyuiopasdfghjklzxcvbnm1234567890@#&_-"
                number = choice(range(0, 6))
                for num in range(0, number):
                    dog_file = requests.get(
                        "https://dog.ceo/api/breeds/image/random", stream=True)
                    dog = requests.get(dog_file.json()["message"], stream=True)
                    image_name = ''.join(
                        choices(key_smith, k=70))+dog_file.json()["message"]
                    params = {
                        "Bucket": S3_BUCKET,
                        "Key": image_name
                    }
                    response = s3_user.generate_presigned_url(
                        'put_object', Params=params, ExpiresIn=5)
                    img_url = response.split('?')[0]
                    img_list.append(img_url)

                    r = requests.put(response, data=dog.raw.read())
                    click.echo()
                    click.echo("status %s" % r.status_code)
                for img in img_list:
                    params = {
                        "img_url": img,
                        "user_id": UUID(post.json()["user_id"]),
                        "post_id": UUID(post.json()["id"])
                    }
                    image = Image(**params)
                    image.create()
                img_count += len(img_list)
                post_arr.append(post)
                post_count += 1
    click.echo(
        '{} posts were added to the database.'.format(post_count))
    click.echo(
        '{} images were added to the database.'.format(img_count))


# burn posts
@burn_cli.command("posts")
@click.option("--amount", default="all", help='number of posts to be deleted')
def post_destroyer(amount):
    posts = [post for post in Post.find_all()]
    if amount == "all":
        amount = len(posts)
    else:
        amount = int(amount)
    count = 0
    if amount > 0:
        for _ in range(0, amount):
            db.session.delete(posts[count])
            db.session.commit()
            count += 1
    click.echo("{} posts where destroyed".format(count))


# seed comments
@seed_cli.command("comments")
def comment_seeder():
    click.echo("...seeding")

    seed(4321)
    count = 0
    posts = [post.json() for post in Post.find_all()]
    users = [user.json() for user in User.find_all()]
    for post in posts:
        if len(post["comments"]) == 0:
            array = [1, 2, 3, 4, 5, 6]
            for num in range(0, choice(array)):
                shuffle(users)
                user = users[0]
                length = choice(range(5, 20))
                body = ""
                while len(body.split(' ')) < length:
                    body = body + " " + Faker().catch_phrase() + "."
                    body = body + " " + Faker().bs().capitalize() + "."
                params = {
                    "body": body,
                    "post_id": post["id"],
                    "user_id": user["id"]
                }
                comment = Comment(**params)
                comment.create()
                count += 1
    click.echo('{} comments were added to the database.'.format(count))


# burn comments
@burn_cli.command("comments")
@click.option("--amount", default="all", help='number of comments to be deleted')
def comment_destroyer(amount):
    comments = [comment for comment in Comment.find_all()]
    if amount == "all":
        amount = len(comments)
    else:
        amount = int(amount)
    count = 0
    if amount > 0:
        for _ in range(0, amount):
            db.session.delete(comments[count])
            db.session.commit()
            count += 1
    click.echo("{} comments where destroyed".format(count))


app.cli.add_command(burn_cli)
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
api.add_resource(comment.Comments, '/comment/<string:id>')
api.add_resource(comment.AllComments, '/comments')

# Post Resource(s)
api.add_resource(post.UserPosts, '/user/posts/<string:id>')
api.add_resource(post.Posts, '/post/<string:id>')
api.add_resource(post.AllPosts, '/posts')

# Image Resource(s)
api.add_resource(image.Images, '/image/<string:id>')
api.add_resource(image.AllImages, '/images')

# File Resource(s)
api.add_resource(fileport.S3Upload, "/s3")
api.add_resource(fileport.S3Delete, "/s3/<string:key>")

# Shelter Resource(s)
api.add_resource(shelter.Shelters, '/shelter/<string:id>')
api.add_resource(shelter.Allshelters, '/shelters')


if __name__ == '__main__':
    app.run()
# debug=True
