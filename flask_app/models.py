from datetime import datetime
from flask_app import db


class SheriffSaleDB(db.Model):
    __tablename__ = "SheriffSale"
    id = db.Column("id", db.Integer, primary_key=True)
    sale_date = db.Column("sale_date", db.String(12))
    county = db.Column("county", db.String(20))
    address = db.Column("address", db.String(100))
    address_sanitized = db.Column("address_sanitized", db.String(30))
    unit = db.Column("unit", db.String(20))
    secondary_unit = db.Column("secondary_unit", db.String(20))
    city = db.Column("city", db.String(20))
    zip_code = db.Column("zip_code", db.String(5))
    sheriff = db.Column("sheriff", db.String(15))
    court_case = db.Column("court_case", db.String(25))
    plaintiff = db.Column("plaintiff", db.String(30))
    defendant = db.Column("defendant", db.String(30))
    priors = db.Column("priors", db.String(100))
    attorney = db.Column("attorney", db.String(100))
    judgment = db.Column("judgment", db.String(20))
    maps_url = db.Column("maps_url", db.String(100))
    # status_history = db.Column('status_history', db.String(100))

    @property
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"""SheriffSaleDB(''{self.sale_date}', '{self.judgment}',
        '{self.address_sanitized}', '{self.unit}', '{self.city}', '{self.zip_code}',
        '{self.sheriff}'"""


class NJParcelsDB(db.Model):
    __tablename__ = "NJParcels"
    id = db.Column("id", db.Integer, primary_key=True)
    city = db.Column("City", db.String(60))
    block = db.Column("Block", db.Integer())
    address = db.Column("Address", db.String(100))
    lot = db.Column("Lot", db.String(15))
