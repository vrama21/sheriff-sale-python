from datetime import datetime
from . import db


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
        return
        f"""
            SheriffSaleDB(''{self.sale_date}', '{self.judgment}',
            '{self.address_sanitized}', '{self.unit}', '{self.city}', '{self.zip_code}',
            '{self.sheriff}'
        """


class NJParcelsDB(db.Model):
    __tablename__ = "NJParcels"
    id = db.Column("id", db.Integer, primary_key=True)
    block = db.Column("Block", db.Integer())
    address = db.Column("Address", db.String(100))
    city = db.Column("City", db.String(60))
    lot = db.Column("Lot", db.String(15))


class CountyClerkDB(db.Model):
    __tablename__ = 'CountyClerk'
    id = db.Column("id", db.Integer, primary_key=True)
    block = db.Column("block", db.String)
    correction_flag = db.Column("correction_flag", db.String)
    cross_party_name = db.Column("cross_party_name", db.String)
    doc_id = db.Column("doc_id", db.String, unique=True)
    doc_status = db.Column("doc_status", db.String)
    doc_type = db.Column("doc_type", db.String)
    file_num = db.Column("file_num", db.String)
    legal_1 = db.Column("legal_1", db.String)
    lot = db.Column("lot", db.String)
    party_code = db.Column("party_code", db.String)
    party_name = db.Column("party_name", db.String)
    pv_no_data = db.Column("pv_no_data", db.String)
    rec_date = db.Column("rec_date", db.String)
    rowid = db.Column("rowid", db.String)
    town = db.Column("town", db.String)


