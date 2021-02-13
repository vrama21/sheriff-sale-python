from .. import db


class SheriffSaleModel(db.Model):
    __tablename__ = 'SheriffSale'
    __table_args__ = {'extend_existing': True}

    id = db.Column('id', db.Integer, primary_key=True)

    address = db.Column('address', db.String)
    address_sanitized = db.Column('address_sanitized', db.String)
    attorney = db.Column('attorney', db.String)
    attorney_phone = db.Column('attorney_phone', db.String)
    city = db.Column('city', db.String)
    county = db.Column('county', db.String)
    court_case = db.Column('court_case', db.String)
    deed = db.Column('deed', db.String)
    deed_address = db.Column('deed_address', db.String)
    defendant = db.Column('defendant', db.String)
    judgment = db.Column('judgment', db.String)
    maps_url = db.Column('maps_url', db.String)
    parcel = db.Column('parcel', db.String)
    plaintiff = db.Column('plaintiff', db.String)
    priors = db.Column('priors', db.String)
    sale_date = db.Column('sale_date', db.String)
    secondary_unit = db.Column('secondary_unit', db.String)
    sheriff = db.Column('sheriff', db.String)
    street = db.Column('street', db.String)
    unit = db.Column('unit', db.String)
    unit_secondary = db.Column('unit_secondary', db.String)
    upset_amount = db.Column('upset_amount', db.String)
    zip_code = db.Column('zip_code', db.String)

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
