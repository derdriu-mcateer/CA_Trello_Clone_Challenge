from flask import Blueprint
from flask_jwt_extended import jwt_required
from setup import db
from models.card import CardSchema, Card
from auth import admin_required


cards_bp = Blueprint('cards', __name__, url_prefix='/cards')


@cards_bp.route("/")
@jwt_required()
def get_cards():
    admin_required()
    #get all the cards from the database table
    stmt = db.select(Card)
    cards = db.session.scalars(stmt).all()
    # Convert the cards from the database into a JSON format and store them in result
    #return result in JSON format
    return CardSchema(many=True).dump(cards)