from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import environ

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = environ.get('JWT_SECRET_KEY')

# set the database URI via SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI')

#create the database object (link the Flask app from line 13 to the database) allowing SQLAlchemy to interact with the db
db = SQLAlchemy(app)

# create an instance of Marshmallow
ma = Marshmallow(app)
# create an instance of Bcrypt
bcrypt = Bcrypt(app)
# create an instance of JWTManager
jwt = JWTManager(app)