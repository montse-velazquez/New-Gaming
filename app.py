#imported libraries
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, post_load
from flask import Flask, request, jsonify
import click
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
    #Creates relationship between the GAME and WISHLIST table
    games = db.relationship('Game', backref='name', lazy=True)
    wishlist = db.relationship('Wishlist', backref='name', lazy=True )

# Game model for setting attributes to the Game Table in our database
class Game(db.Model):
    # Primary Key of the Game Table
    id = db.Column(db.Integer, primary_key=True)
    #Attributes of the Game Table
    game_name = db.Column(db.String(50))
    game_type = db.Column(db.String(50))
    #Creates Foreign Keys that will be related to the NAME and relationship to the REVIEW table
    name_id = db.Column(db.Integer, db.ForeignKey('name.id'))
    reviews = db.relationship('Review', backref='game', lazy=True)

# Review model for setting attributes to the Review Table in our database
class Review(db.Model):
     # Primary Key of the Review Table
    id = db.Column(db.Integer, primary_key=True)
    #Creates Foreign Keys that will be related to the GAME
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    #Attributes of the Review Table
    rate = db.Column(db.Integer)
    comment = db.Column(db.String(200))

# Wishlist model for setting attributes to the Wishlist Table in our database
class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wish_name = db.Column(db.String())
    wish_type = db.Column(db.String())
    #Creates Foreign Keys that will be related to the NAME
    name_id = db.Column(db.Integer(), db.ForeignKey('name.id'))



# SCHEMAS 

# Name Schema created having in mind the Name attributes
class NameSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    # Explains how the data will be nested inside of the table 
    games = fields.Nested('GameSchema', many=True, exclude = ('reviews', ))
    wish = fields.Nested('WishlistSchema', many=True )

# Game Schema created having in mind the Game attributes
class GameSchema(Schema):
    id = fields.Int()
    game_name = fields.Str()
    game_type = fields.Str()
    name_id = fields.Int()
    # Explains how the data will be nested inside of the table 
    reviews = fields.Nested('ReviewSchema', many=True )

    # Decorator: Loads data
    @post_load
    def make_game(self, data, **kwargs):
        return Game(**data)

# Review Schema created having in mind the Review attributes
class ReviewSchema(Schema):
    id = fields.Int()
    # Explains how the data will be nested inside of the table 
    game_id = fields.Int()
    rate = fields.Int()
    comment = fields.Str()

    # Decorator: Loads data
    @post_load
    def make_game(self, data, **kwargs):
        return Review(**data)


# Wishlist Schema created having in mind the Wishlist attributes
class WishlistSchema(Schema):
    id = fields.Int()
    wish_name = fields.Str()
    wish_type = fields.Str()
    name_id = fields.Int()

    # Decorator: Loads data 
    @post_load
    def make_game(self, data, **kwargs):
        return Wishlist(**data)

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
    game1 = Game(game_name='Fortnite', game_type="Battle royale", name=user1)
    review1 = Review(game = game1, rate = 10, comment = "Nice enviroment")
    wishlist1 = Wishlist(wish_name = "Legacy", wish_type = "open-world", name = user1)

    db.session.add_all([user1, game1, review1, wishlist1])
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

#Create '/game' route with the 'GET' method for retrieving all the information stored in GAME Table
@app.route('/game', methods=['GET'])
def get_games():
    game = Game.query.all()
    game_schema = GameSchema(many=True)
    return jsonify(game_schema.dump(game))

#Create '/game' route with the 'POST' method for posting data inside of the GAME Table
@app.route('/game', methods=['POST'])
def add_game():
    game_schema = GameSchema()
    game = game_schema.load(request.json)
    db.session.add(game)
    db.session.commit()
    return jsonify(game_schema.dump(game)),201

#Create '/review' route with the 'GET' method for retrieving all the information stored in REVIEW Table
@app.route('/review', methods=['GET'])
def get_reviews():
    review = Review.query.all()
    review_schema = ReviewSchema(many=True)
    return jsonify(review_schema.dump(review))

#Create '/review' route with the 'POST' method for posting data inside of the REVIEW Table
@app.route('/review', methods=['POST'])
def add_review():
    review_schema = ReviewSchema()
    review = review_schema.load(request.json)
    db.session.add(review)
    db.session.commit()
    return jsonify(review_schema.dump(review)),201

#Create '/update_review' route with the 'PUT' method for updating data inside of the REVIEW Table 
@app.route('/update_review/<int:game_id>', methods=['PUT'])
def update_review(game_id):
    review = Review.query.get(game_id)
    if review:
        review.rate = request.json['rate']
        review.comment = request.json['comment']
        db.session.commit()
        return jsonify({'message': 'Review created successfully!'}), 202
    else:
        return jsonify({'message': 'Game does not exist'}), 404
    
#Create '/delete_review' route with the 'DELETE' method for deleting single data is inside of the REVIEW Table 
@app.route('/delete_review/<int:game_id>', methods=['DELETE'])
def delete_review(game_id):
    review = Review.query.get(game_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return jsonify({'message': 'Review deleted successfully!'}), 202
    else:
        return jsonify({'message': 'Game does not exist'}), 404

#Create '/wishlist' route with the 'GET' method for retrieving all the information stored in WISHLIST Table
@app.route('/wishlist', methods=['GET'])
def get_wishlist():
    wishlist = Wishlist.query.all()
    wishlist_schema = WishlistSchema(many=True)
    return jsonify(wishlist_schema.dump(wishlist))

#Create '/wishlist' route with the 'POST' method for adding data into the WISHLIST Table
@app.route('/wishlist', methods=['POST'])
def add_wishlist():
    wishlist_schema = WishlistSchema()
    wishlist= wishlist_schema.load(request.json)
    db.session.add(wishlist)
    db.session.commit()
    return jsonify(wishlist_schema.dump(wishlist)),201

#Create '/delete_wishlist' route with the 'DELETE' method for deleting single data inside the WISHLIST Table
@app.route('/delete_wishlist/<string:wish_id>', methods=['DELETE'])
def delete_wishlist(wish_id):
    wish = Wishlist.query.get(wish_id)
    if wish:
        db.session.delete(wish)
        db.session.commit()
        return jsonify({'message': 'WishList item was deleted successfully!'}), 202
    else:
        return jsonify({'message': 'Game does not exist'}), 404


# Runs program 
if __name__ == '__main__':
    app.run(debug=True)

