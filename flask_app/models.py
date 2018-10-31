from flask_app import db
from sqlalchemy import Integer, String


class SheriffSale(db.Model):

    id = db.Column('id', db.Integer, primary_key=True)
    sheriff = db.Column('sheriff', db.String(15))
    court_case = db.Column('court_case', db.String(15))
    sale_date = db.Column('sale_date', db.String(10))
    plaintiff = db.Column('plaintiff', db.String(30))
    defendant = db.Column('defendant', db.String(30))
    address = db.Column('address', db.String(100))
    priors = db.Column('priors', db.String(100))
    attorney = db.Column('attorney', db.String(100))
    judgment = db.Column('judgment', db.String(20))
    deed = db.Column('deed', db.String(50))
    deed_address = db.Column('deed_address', db.String(30))
    maps_href = db.Column('maps_href', db.String(100))
    # status_history = db.Column('status_history', db.String(100))
    address_sanitized = db.Column('address_sanitized', db.String(30))
    unit = db.Column('unit', db.String(20))
    city = db.Column('city', db.String(20))
    zip_code = db.Column('zip_code', db.String(5))

    def __repr__(self):
        return f"""SheriffSale('{sheriff}', '{court_case}', '{sale_date}',
        '{plaintiff}', '{defendant}', '{address}', '{priors}', '{attorney}',
        '{judgment}', '{deed}', '{deed_address}', '{maps_href}', 
        '{address_sanitzed}', '{unit}', '{city}', '{zip_code}'"""



class NJParcelsDB(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    city = db.Column('City', db.String(60))
    block = db.Column('Block', db.Integer())
    address = db.Column('Address', db.String(100))
    lot = db.Column('Lot', db.String(15))
