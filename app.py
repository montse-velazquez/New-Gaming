from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from flask import Flask
from flask.cli import with_appcontext

app = Flask(__name__)
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://montsevelazquez:myPassword@localhost:5432/gaming"
db.init_app(app)

class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))

class NameSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()

app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Table created')

@app.cli.command("db_seed")
@with_appcontext
def seed_command():
    user1 = Name(username='John98', first_name="John", last_name="DB")

    db.session.add_all([user1, ])
    db.session.commit()
    print('Data seeded successfully.')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("Table dropped")

    

if __name__ == '__main__':
    app.run(debug=True)

