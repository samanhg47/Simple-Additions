import requests
from resources import fileport, shelter, image, post, state, user, auth, comment, admin, city
from random import shuffle, seed, choices, choice
from faker.providers.person.en import Provider
from sheets.read.shelters import all_shelters
from sheets.read.states import states_list
from sheets.read.cities import cities_list
from middleware import check_token, gen_password, strip_secret
from models.shelter import Shelter
from models.comment import Comment
from flask_migrate import Migrate
from models.state import State
from models.city import City
from models.image import Image
from flask.cli import AppGroup
from dotenv import load_dotenv
from flask_restful import Api
from models.user import User
from models.post import Post
from flask_cors import CORS
from flask import request, Response
from models.db import db
from gevent import sleep
from flask import Flask
from faker import Faker
from uuid import UUID
import click
import boto3
import os


app = Flask(__name__)
CORS(app)

api = Api(app)
seed_cli = AppGroup("seed")
burn_cli = AppGroup("burn")

load_dotenv()
S3_BUCKET = os.getenv("S3_BUCKET")
S3_USER_ID = os.getenv("S3_USER_ID")
S3_USER_SECRET = os.getenv("S3_USER_SECRET")
S3_REGION = os.getenv("S3_REGION")

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL.replace(
        "://", "ql://", 1)
    app.config['SQLALCHEMY_ECHO'] = False
    app.env = 'production'
else:
    app.debug = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/simple_additions_db'
    app.config['SQLALCHEMY_ECHO'] = True


# seed states
@seed_cli.command("states")
def state_seeder():
    if len(State.find_all()) == 0:
        count = 0
        for state in states_list:
            state = State(**state)
            state.create()
            count += 1
    click.echo("{} states were added to the database.".format(count))


# burn state
@burn_cli.command("states")
def state_destroyer():
    if len(State.find_all()) > 0:
        count = 0
        for state in State.find_all():
            db.session.delete(state)
            db.session.commit()
            count += 1
    click.echo("{} states were destroyed.".format(count))


# seed cities
@seed_cli.command("cities")
def city_seeder():
    if len(City.find_all()) == 0:
        count = 0
        states = [state.json() for state in State.find_all()]
        for city in cities_list:
            for state in states:
                state_name = state["shorthand"]
                state_id = state["id"]
                if city["state_name"] == state_name:
                    city["state_id"] = state_id
                    this_city = City(**city)
                    this_city.create()
                    count += 1
    click.echo("{} cities were added to the database.".format(count))


# burn cities
@burn_cli.command("cities")
def city_destroyer():
    if len(City.find_all()) > 0:
        count = 0
        for city in City.find_all():
            db.session.delete(city)
            db.session.commit()
            count += 1
    click.echo("{} cities were destroyed.".format(count))


# seed users
@seed_cli.command("users")
@click.option('--amount', default=47, help='number of users to be generated')
def user_seeder(amount):
    if amount > 0:
        if amount == 47:
            amount = len(Shelter.find_all())/4
        first_names = list(set(Provider.first_names))
        last_names = list(set(Provider.last_names))
        seed(4321)
        shuffle(first_names)
        shuffle(last_names)
        random_usernames = []
        random_emails = []

        click.echo('seeding...')

        def name_check(name):
            if name in random_usernames:
                new_name = choice(first_names)+"_" + \
                    choice(last_names) + num_tail()
                name_check(new_name)
            else:
                return name

        def num_tail():
            str = "123456789"
            address = ""
            num = choice(str[1:4])[0]
            for char in choices(str, k=int(num)):
                address += char
            return address

        for i in range(0, amount):
            name = choice(first_names)+"_"+choice(last_names) + num_tail()
            new_name = name_check(name)
            random_usernames.insert(0, new_name)
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
@click.option('--state', default="all", help='number of shelters to be generated')
def shelter_seeder(state):
    click.echo('seeding...')
    count = 0
    shelter_list = []
    if state == "all":
        for shelter in all_shelters:
            if not Shelter.by_address(shelter['shelter_name'], shelter['address']):
                if City.by_info(shelter['state'], shelter['city'], shelter['zipcode']):
                    city_id = City.by_info(
                        shelter['state'], shelter['city'], shelter['zipcode']).json()['id']
                    shelter_name = shelter['shelter_name']
                    password_digest = gen_password(shelter['password'])
                    email = shelter['email']
                    address = shelter['address']
                    phone_number = shelter['phone_number']
                    latitude = shelter['latitude']
                    longitude = shelter['longitude']
                    this_model = Shelter(
                        shelter_name, address, city_id, email,
                        phone_number, latitude, longitude, password_digest
                    )
                    this_model.create()
                    shelter_list.append(this_model)
                    count += 1
    else:
        for shelter in all_shelters:
            if not Shelter.by_address(shelter['shelter_name'], shelter['address']) \
                    and shelter["state"] == state:
                if City.by_info(shelter['state'], shelter['city'], shelter['zipcode']):
                    city_id = City.by_info(
                        shelter['state'], shelter['city'], shelter['zipcode']).json()['id']
                    shelter_name = shelter['shelter_name']
                    password_digest = gen_password(shelter['password'])
                    email = shelter['email']
                    address = shelter['address']
                    phone_number = shelter['phone_number']
                    latitude = shelter['latitude']
                    longitude = shelter['longitude']
                    this_model = Shelter(
                        shelter_name, address, city_id, email,
                        phone_number, latitude, longitude, password_digest
                    )
                    this_model.create()
                    shelter_list.append(this_model)
                    count += 1

    click.echo(
        '{} shelters were added to the database.'.format(count))


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
                        'put_object', Params=params, ExpiresIn=15)
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

db.init_app(app)
migrate = Migrate(app, db)


@app.before_request
def acceptable_origins():
    if request.origin == "https://simple-additions.netlify.app":
        if request.method != "OPTIONS":
            if strip_secret(request):
                if 'login' not in request.path and 'register' not in request.path\
                        and 'cit' not in request.path and 'state' not in request.path:
                    if not check_token(request):
                        return Response("Please Login", status=401, mimetype='application/json')
            else:
                return Response('Oops, Try Again 😊', status=401, mimetype='application/json')
    else:
        return Response('Oops, Try Again 😊', status=401, mimetype='application/json')


@app.after_request
def after_request(response):
    print()
    print()
    print()
    print(response.headers)
    print()
    print()
    print()
    click.echo(response.headers)
    response.headers.add(
        'Access-Control-Allow-Origin',
        'https://simple-additions.netlify.app'
    )
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization,Secret,Set-Cookie'
    )
    response.headers.add(
        'Access-Control-Allow-Methods',
        '*'
    )
    response.headers.add(
        'Access-Control-Allow-Credentials', 'true'
    )
    return response


# Auth Resource(s)
api.add_resource(auth.ShelterRegister, '/api/register/shelters')
api.add_resource(auth.ShelterLogin, '/api/login/shelters')
api.add_resource(auth.UserRegister, '/api/register/users')
api.add_resource(auth.UserLogin, '/api/login/users')
api.add_resource(auth.Token, '/api/token')

# Admin Resource(s)
api.add_resource(admin.AdminAllShelters, '/api/admin/shelters')
api.add_resource(admin.AdminAllComments, '/api/admin/comments')
api.add_resource(admin.AdminAllImages, '/api/admin/images')
api.add_resource(admin.AdminAllUsers, '/api/admin/users')
api.add_resource(admin.AdminAllPosts, '/api/admin/posts')

# User Resource(s)
api.add_resource(user.Users, '/api/user/<string:id>')
api.add_resource(user.AllUsers, '/api/users')

# Comment Resource(s)
api.add_resource(comment.UserComments, '/api/user/comments/<string:id>')
api.add_resource(comment.Comments, '/api/comment/<string:id>')
api.add_resource(comment.AllComments, '/api/comments')

# Post Resource(s)
api.add_resource(post.UserPosts, '/api/user/posts/<string:id>')
api.add_resource(post.Posts, '/api/post/<string:id>')
api.add_resource(post.AllPosts, '/api/posts')

# Image Resource(s)
api.add_resource(image.Images, '/api/image/<string:id>')
api.add_resource(image.AllImages, '/api/images')

# File Resource(s)
api.add_resource(fileport.S3Upload, '/api/s3')
api.add_resource(fileport.S3Delete, '/api/s3/<string:key>')

# Shelter Resource(s)
api.add_resource(shelter.Shelters, '/api/shelter/<string:id>')
api.add_resource(shelter.By_Proximity, '/api/shelters')

# City Resource(s)
api.add_resource(city.By_State, '/api/cities/<string:state>')
api.add_resource(city.City_Id, '/api/city/<string:id>')
api.add_resource(
    city.Detailed, '/api/city/<string:state>/<string:name>/<int:zipcode>')

# State Resource(s)
api.add_resource(state.States, '/api/states')
api.add_resource(state.By_Short, '/api/state/<string:state>')
api.add_resource(state.State_Id, '/api/state/<string:id>')


if __name__ == '__main__':
    app.run()
