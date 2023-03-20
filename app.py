#imported libraries
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from flask import Flask, jsonify
from flask.cli import with_appcontext


app = Flask(__name__)
db = SQLAlchemy()

# Make coonnection with the database, in this case this is the one used while making the project for making connection with your own database follow the syntax -->
# URI Syntax: "[database] + "://" + [database user] + ":" + [password] + "@localhost:5432/" [database-name]"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://montsevelazquez:myPassword@localhost:5432/gaming"
db.init_app(app)

# Name model for setting attributes to the Name Table in our database
class Name(db.Model):
    # Primary Key of the Name Table
    id = db.Column(db.Integer, primary_key=True)
    #Attributes of the Name Table
    username = db.Column(db.String(50))
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(50))
    game_type = db.Column(db.String(50))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer)
    comment = db.Column(db.String(200))

# SCHEMAS 

# Name Schema created having in mind the Name attributes
class NameSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()

class GameSchema(Schema):
    id = fields.Int()
    game_name = fields.Str()
    game_type = fields.Str()

class ReviewSchema(Schema):
    id = fields.Int()
    rate = fields.Int()
    comment = fields.Str()

#CLI COMMANDS

#CLI commands used for being user friendly and interact with the database and tables, each command has to be written inside of the terminal
# 'db_create' command will create the tables that were settled woth the Models
app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Table created')

# 'db_seed' command will seed all the data that we will like to initiate with
@app.cli.command("db_seed")
@with_appcontext
def seed_command():
    user1 = Name(username='John98', first_name="John", last_name="DB")
    game1 = Game(game_name='Fortnite', game_type="Battle royale")
    review1 = Review(rate = 10, comment = "Nice enviroment")

    db.session.add_all([user1, game1, review1])
    db.session.commit()
    print('Data seeded successfully.')

# 'db_drop' command will drop all the tables stored in the database 
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("Table dropped")


# ROUTES

#Create '/name' route with the 'GET' method for retrieving all the information stored in NAME Table
@app.route('/name', methods=['GET'])
def get_name():
    name = Name.query.all()
    name_schema = NameSchema(many=True)
    return jsonify(name_schema.dump(name)) 

@app.route('/game', methods=['GET'])
def get_games():
    game = Game.query.all()
    game_schema = GameSchema(many=True)
    return jsonify(game_schema.dump(game))

@app.route('/review', methods=['GET'])
def get_reviews():
    review = Review.query.all()
    review_schema = ReviewSchema(many=True)
    return jsonify(review_schema.dump(review))


# Runs program 
if __name__ == '__main__':
    app.run(debug=True)

