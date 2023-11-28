from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required
from setup import db
from models.card import CardSchema, Card
from auth import admin_required


cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

# Get all cards 
@cards_bp.route("/")

def get_cards():
    admin_required()
    #get all the cards from the database table
    stmt = db.select(Card)
    cards = db.session.scalars(stmt).all()
    # Convert the cards from the database into a JSON format and store them in result
    #return result in JSON format
    return CardSchema(many=True).dump(cards)

#Get one card
@cards_bp.route('/<int:id>')
@jwt_required()
def one_card(id):
    admin_required()
    stmt = db.select(Card).filter_by(id=id) #.where (Card.id == id)
    card = db.session.scalar(stmt)
    if card:
        return CardSchema().dump(card)
    else:
        return {'error': 'Card not found'}, 404
    
# Create a new card
#     # uses the CardSchema to deserialise the JSON data into a python dictionary (card_info)
#     # this step validated and loads the incoming JSON data based on the schema defined in 'CardSchema'
@cards_bp.route('/', methods=['POST'])
@jwt_required()
def create_card():
    admin_required()
    card_info = CardSchema(exclude=['id', 'date_created']).load(request.json)
    card = Card(
        title = card_info['title'],
        description = card_info.get('description', ''),
        status = card_info.get('status','To Do')
    )
    db.session.add(card)
    db.session.commit()
    return CardSchema().dump(card),201 
    

# Update a card 
@cards_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_card(id):
    admin_required()
    card_info = CardSchema(exclude=['id', 'date_created']).load(request.json)
    stmt = db.select(Card).filter_by(id=id) 
    card = db.session.scalar(stmt)
    if card:
        card.title = card_info.get('title', card.title)
        card.description = card_info.get('description', card.description)
        card.status = card_info.get('status', card.status)
        db.session.commit()
        return CardSchema().dump(card), 200
    else:
        return {'error': 'Card not found'}, 404


# Delete a card
@cards_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_card(id):
    admin_required()
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        db.session.delete(card)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'Card not found'}, 404


