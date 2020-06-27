from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f257b913bf5f06fc9680179dbc27f867'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
s = Serializer(app.config['SECRET_KEY'], 1800)

from app import routes
