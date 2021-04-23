from .. import db
from decimal import Decimal


class Listing(db.Model):
    __tablename__ = 'listing'
    __table_args__ = {'extend_existing': True}

    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    sheriff_id = db.Column('sheriff_id', db.String)

    address = db.Column('address', db.String, unique=True)
    attorney = db.Column('attorney', db.String)
    attorney_phone = db.Column('attorney_phone', db.String)
    city = db.Column('city', db.String)
    county = db.Column('county', db.String)
    court_case = db.Column('court_case', db.String)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    deed = db.Column('deed', db.String)
    deed_address = db.Column('deed_address', db.String)
    defendant = db.Column('defendant', db.String)
    description = db.Column('description', db.String)
    judgment = db.Column('judgment', db.Numeric(10, 2))
    latitude = db.Column('latitude', db.String)
    longitude = db.Column('longitude', db.String)
    maps_url = db.Column('maps_url', db.String)
    parcel = db.Column('parcel', db.String)
    plaintiff = db.Column('plaintiff', db.String)
    priors = db.Column('priors', db.String)
    raw_address = db.Column('raw_address', db.String)
    sale_date = db.Column('sale_date', db.String)
    secondary_unit = db.Column('secondary_unit', db.String)
    state = db.Column('state', db.String)
    status_history = db.relationship('StatusHistory', backref='StatusHistory', lazy=True)
    street = db.Column('street', db.String)
    unit = db.Column('unit', db.String)
    unit_secondary = db.Column('unit_secondary', db.String)
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    upset_amount = db.Column('upset_amount', db.Numeric(10, 2))
    zip_code = db.Column('zip_code', db.String)

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

    id = db.Column('id', db.Integer, primary_key=True, nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))

    status = db.Column('status', db.String)
    date = db.Column('date', db.String)

    @property
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
