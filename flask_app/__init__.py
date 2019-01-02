from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sheriff_sale import SheriffSale
from nj_parcels import NJParcels

app = Flask(__name__)
app.config['SECRET_KEY'] = '17a202d87bb99ee84fd5ebbec5130e0f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

db = SQLAlchemy(app)

sheriff_sale = SheriffSale()
nj_parcels = NJParcels()

from flask_app import routes
