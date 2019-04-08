from datetime import datetime
from flask_app import db

date_created = datetime.today().strftime('%m-%d-%Y')

# class CustomModel(db.Model):
#     id = db.Column('id', db.Integer, primary_key=True)
#     # __table__ = SheriffSaleDB
#     # __mapper_args__ = {
#     #     'primary_key': [SheriffSaleDB.id]
#     # }
#
#     def __init__(self):
#         self.date_created = datetime.today().strftime('%m-%d-%Y')


class SheriffSaleDB(db.Model):
    __tablename__ = f"Sheriff Sale {date_created}"
    id = db.Column('id', db.Integer, primary_key=True)
    sheriff = db.Column('sheriff', db.String(15))
    court_case = db.Column('court_case', db.String(25))
    sale_date = db.Column('sale_date', db.String(12))
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
    secondary_unit = db.Column('secondary_unit', db.String(20))
    city = db.Column('city', db.String(20))
    zip_code = db.Column('zip_code', db.String(5))

    def __repr__(self):
        return f"""SheriffSaleDB(''{self.sale_date}', '{self.judgment}',
        '{self.address_sanitized}', '{self.unit}', '{self.city}', '{self.zip_code}',
        '{self.sheriff}'"""


class NJParcelsDB(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    city = db.Column('City', db.String(60))
    block = db.Column('Block', db.Integer())
    address = db.Column('Address', db.String(100))
    lot = db.Column('Lot', db.String(15))
