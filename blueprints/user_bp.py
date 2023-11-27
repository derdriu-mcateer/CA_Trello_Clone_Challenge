from flask import Blueprint, request, abort
from models.user import User, UserSchema
from setup import bcrypt, db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from datetime import timedelta


users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route("/register", methods=["POST"])
def register():
    # uses the UserSchema to deserialise the JSON data into a python dictionary (user_info)
    # this step validated and loads the incoming JSON data based on the schema defined in 'UserSchema'
    user_info = UserSchema(exclude=['id', 'admin']).load(request.json)
    # find the user by email address
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)

    if user:
        # return an abort message to inform the user. That will end the request
        return abort(400, description="Email already registered")
    # Create the user object
    # creates a new user object using the User model and extracts the relevant information from the user_info dictionary
    user = User(
        email=user_info['email'],
        # add password with hashing
        password=bcrypt.generate_password_hash(user_info['password']).decode('utf8'),
        name = user_info.get('name', '')
        )
    # add and commit the new user to the database
    db.session.add(user)
    db.session.commit()
    #Return the user to check the request was successful
    return UserSchema(exclude=['password']).dump(user), 201

@users_bp.route("/login", methods=["POST"])
def login():
    # parse incoming POST body through the schema
    user_info = UserSchema(exclude=['id', 'name', 'admin']).load(request.json)
    # find the user in the database via email address
    stmt = db.select(User).filter_by(email = user_info["email"])
    user = db.session.scalar(stmt)
    if  user and bcrypt.check_password_hash(user.password, user_info["password"]):
        token = create_access_token(identity=user.email, expires_delta=timedelta(hours=2))
        return {'user': UserSchema(exclude=['password']).dump(user),'token': token}
    else:
        return {"error": "Invalid email or password"}, 401