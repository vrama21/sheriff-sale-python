from .. import db


class NJParcelsModel(db.Model):
    __tablename__ = 'nj_parcels'
    __table_args__ = {'extend_existing': True}

    id = db.Column('id', db.Integer, primary_key=True)
    sheriff_sale_id = db.Column(db.Integer, db.ForeignKey('sheriff_sale.id'))

    address = db.Column('address', db.String)
    block = db.Column('block', db.Integer)
    city = db.Column('city', db.String)
    county = db.Column('county', db.String)
    lot = db.Column('lot', db.String)

    @property
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
