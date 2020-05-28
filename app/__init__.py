from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f257b913bf5f06fc9680179dbc27f867'

from app import routes
