from .. import db
from decimal import Decimal
from datetime import datetime


class Listing(db.Model):
    __tablename__ = 'listing'
    __table_args__ = {'extend_existing': True}

    id: int = db.Column('id', db.Integer, primary_key=True, nullable=False)
    sheriff_id: str = db.Column('sheriff_id', db.String)

    address: str = db.Column('address', db.String, unique=True)
    attorney: str = db.Column('attorney', db.String)
    attorney_phone: str = db.Column('attorney_phone', db.String)
    city: str = db.Column('city', db.String)
    county: str = db.Column('county', db.String)
    court_case: str = db.Column('court_case', db.String)
    created_on: datetime = db.Column(db.DateTime, server_default=db.func.now())
    deed: str = db.Column('deed', db.String)
    deed_address: str = db.Column('deed_address', db.String)
    defendant: str = db.Column('defendant', db.String)
    description: str = db.Column('description', db.String)
    judgment: float = db.Column('judgment', db.Numeric(10, 2))
    latitude: str = db.Column('latitude', db.String)
    longitude: str = db.Column('longitude', db.String)
    maps_url: str = db.Column('maps_url', db.String)
    parcel: str = db.Column('parcel', db.String)
    plaintiff: str = db.Column('plaintiff', db.String)
    priors: str = db.Column('priors', db.String)
    raw_address: str = db.Column('raw_address', db.String)
    sale_date: str = db.Column('sale_date', db.String)
    secondary_unit: str = db.Column('secondary_unit', db.String)
    state: str = db.Column('state', db.String)
    status_history = db.relationship('StatusHistory', backref='StatusHistory', lazy=True)
    street: str = db.Column('street', db.String)
    unit: str = db.Column('unit', db.String)
    unit_secondary: str = db.Column('unit_secondary', db.String)
    updated_on: datetime = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    upset_amount: float = db.Column('upset_amount', db.Numeric(10, 2))
    zip_code: str = db.Column('zip_code', db.String)

    @property
    def serialize(self):
        serialized_dict = {}

        for column in self.__table__.columns:
            value = getattr(self, column.name)

            if isinstance(value, Decimal):
                value = float(value)

            serialized_dict[column.name] = value

        return serialized_dict


class StatusHistory(db.Model):
    __tablename__ = 'status_history'
    __table_args__ = {'extend_existing': True}

    id: int = db.Column('id', db.Integer, primary_key=True, nullable=False)
    listing_id: int = db.Column(db.Integer, db.ForeignKey('listing.id'))

    status: str = db.Column('status', db.String)
    date: str = db.Column('date', db.String)

    @property
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
