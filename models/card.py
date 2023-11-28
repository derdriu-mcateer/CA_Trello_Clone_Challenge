from setup import db, ma
from datetime import datetime

# By inheriting from db.Model, the Card class gains functionalities and features from SQLAlchemy's ORM, 
# allowing it to map Python objects to corresponding database tables.
class Card(db.Model):
    # define the table name for the db
    __tablename__= "cards"
    # Set the primary key, we need to define that each attribute is also a column in the db table, remember "db" is the object we created in the previous step.
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(30), default='To Do')
    date_created = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))

#create the Card Schema with Marshmallow, 
#it will provide the serialization needed for converting the data into JSON
class CardSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "title", "description", "status", "date_created")
