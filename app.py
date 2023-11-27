# import Flask and request from the Flask framework
from flask import request, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from setup import *
from models.user import User, UserSchema
from models.card import Card, CardSchema
from blueprints.cli_bp import db_commands
from blueprints.user_bp import users_bp



def admin_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).where(User.email == user_email)
    user = db.session.scalar(stmt)
    if not (user and user.admin):
        abort(401)

@app.errorhandler(401)
def unauthorised(err):
    return {'error': 'You must be an admin'}

app.register_blueprint(db_commands)

app.register_blueprint(users_bp)

@app.route("/cards")
@jwt_required()
def get_cards():
    admin_required()
    #get all the cards from the database table
    stmt = db.select(Card)
    cards = db.session.scalars(stmt).all()
    # Convert the cards from the database into a JSON format and store them in result
    #return result in JSON format
    return CardSchema(many=True).dump(cards)

@app.route("/")
def hello():
  return "Hello World!"






