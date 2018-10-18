from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sheriff_sale import SheriffSale
from nj_parcel_parser import ParseNJParcels
# from database import Database
# from database_models import SheriffSaleDB, NJParcelsDB

app = Flask(__name__)
app.config['SECRET_KEY'] = '17a202d87bb99ee84fd5ebbec5130e0f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_BINDS'] = {
    'sheriff_sale': 'sqlite:///sheriff_sale.db',
    'nj_parcels': 'sqlite:///nj_parcels.db'
}

db = SQLAlchemy(app)

sheriff_sale = SheriffSale()
# sheriff_sale_db = Database('sheriff_sale.db', SheriffSaleDB)
nj_parcels = ParseNJParcels()
# nj_parcels_db = Database('nj_parcels.db', NJParcelsDB)

from flask_app import routes
