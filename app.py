from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://montsevelazquez:myPassword@localhost:5432/gaming"
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)