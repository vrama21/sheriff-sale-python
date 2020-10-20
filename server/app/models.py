from datetime import datetime
from . import db


class SheriffSaleModel(db.Model):
    __tablename__ = 'SheriffSale'
    __table_args__ = {'extend_existing': True}

    id = db.Column('id', db.Integer, primary_key=True)

    address = db.Column('address', db.String)
    address_sanitized = db.Column('address_sanitized', db.String)
    attorney = db.Column('attorney', db.String)
    city = db.Column('city', db.String)
    county = db.Column('county', db.String)
    court_case = db.Column('court_case', db.String)
    defendant = db.Column('defendant', db.String)
    judgment = db.Column('judgment', db.String)
    maps_url = db.Column('maps_url', db.String)
    plaintiff = db.Column('plaintiff', db.String)
    priors = db.Column('priors', db.String)
    sale_date = db.Column('sale_date', db.String)
    secondary_unit = db.Column('secondary_unit', db.String)
    sheriff = db.Column('sheriff', db.String)
    unit = db.Column('unit', db.String)
    zip_code = db.Column('zip_code', db.String)

    # nj_parcels_id = db.Column(db.Integer, db.ForeignKey('NJParcels.id'))
    # nj_parcels = db.relationship('NJParcelsModel', uselist=False, backref='SheriffSale', foreign_keys=[nj_parcels_id])
    # status_history = db.relationship('StatusHistoryModel', uselist=False, backref='SheriffSale')

    @property
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class StatusHistoryModel(db.Model):
    __tablename__ = 'StatusHistory'
    __table_args__ = {'extend_existing': True}


    id = db.Column('id', db.Integer, primary_key=True)
    # sheriff_sale_id = db.Column(db.Integer, db.ForeignKey('SheriffSale.id'))

    status = db.Column('status', db.String)
    date = db.Column('date', db.String)


class NJParcelsModel(db.Model):
    __tablename__ = 'NJParcels'
    __table_args__ = {'extend_existing': True}

    id = db.Column('id', db.Integer, primary_key=True)
    sheriff_sale_id = db.Column(db.Integer, db.ForeignKey('SheriffSale.id'))

    address = db.Column('address', db.String)
    block = db.Column('block', db.Integer)
    city = db.Column('city', db.String)
    county = db.Column('county', db.String)
    lot = db.Column('lot', db.String)

    @property
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CountyClerkModel(db.Model):
    __tablename__ = 'CountyClerk'
    __table_args__ = {'extend_existing': True}

    id = db.Column('id', db.Integer, primary_key=True)
    block = db.Column('block', db.String)
    correction_flag = db.Column('correction_flag', db.String)
    cross_party_name = db.Column('cross_party_name', db.String)
    doc_id = db.Column('doc_id', db.String, unique=True)
    doc_status = db.Column('doc_status', db.String)
    doc_type = db.Column('doc_type', db.String)
    file_num = db.Column('file_num', db.String)
    legal_1 = db.Column('legal_1', db.String)
    lot = db.Column('lot', db.String)
    party_code = db.Column('party_code', db.String)
    party_name = db.Column('party_name', db.String)
    pv_no_data = db.Column('pv_no_data', db.String)
    rec_date = db.Column('rec_date', db.String)
    rowid = db.Column('rowid', db.String)
    town = db.Column('town', db.String)

    @property
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

