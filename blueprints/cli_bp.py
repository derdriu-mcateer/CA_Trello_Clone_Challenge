from flask import Blueprint
from setup import db, bcrypt
from models.card import Card
from models.user import User
from datetime import date

db_commands = Blueprint('db', __name__)

# create app's cli command named create, then run it in the terminal as "flask create", 
# it will invoke create_db function
@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("seed")
def seed_db():
    from datetime import date
    # create the first card object
    cards = [
        Card(
            title="Start the project",
            description="Stage 1 - ERD Creation",
            status="Done",
            date_created=date.today(),
        ),
        Card(
            title="ORM Queries",
            description="Stage 2 - Implement CRUD queries",
            status="In Progress",
            date_created=date.today(),
        ),
        Card(
            title="Marshmallow",
            description="Stage 3 - Implement JSONify of models",
            status="In Progress",
            date_created=date.today(),
        ),
    ]

    db.session.add_all(cards)

    users = [
        User(
            email='admin@spam.com',
            password = bcrypt.generate_password_hash("spinynorman").decode("utf-8"),
            admin=True
        ),
        User(
            name = 'John Cleese',
            email = 'cleese@spam.com',
            password = bcrypt.generate_password_hash("123").decode("utf-8")
        )
    ]

    # Add all instances of User to the table
    db.session.add_all(users)
    
    # commit the changes
    db.session.commit()
    print("Table seeded")  

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 

    # db.session.add(card1)