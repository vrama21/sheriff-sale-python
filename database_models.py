from flask_app import db
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table, DateTime
from sqlalchemy.ext.automap import automap_base
from base import Base

engine = create_engine('sqlite:///nj_parcels.db')
metadata = MetaData()
metadata.clear()
metadata.reflect(engine)


class SheriffSaleDB(db.Model):

    # TODO: Submit sales_date text from site to the __tablename__ string
    __tablename__ = 'sheriff_sale'
    id = db.Column('id', Integer, primary_key=True)
    sheriff = db.Column('sheriff', String(15))
    sale_date = db.Column('sale_date', DateTime(15))
    plaintiff = db.Column('plaintiff', String(30))
    defendant = db.Column('defendant', String(30))
    address = db.Column('address', String(100))

    def __repr__(self):
        return f'<Data(sheriff={self.sheriff}, sale_date={self.sale_date}, plaintiff={self.plaintiff},' \
               f'defendant={self.defendant}, address={self.address})>'


class NJParcelsDB(db.Model):
    __tablename__ = Table('Atlantic', Base.metadata, autoload=True, autoload_with=engine)
    # id = db.Column('id', Integer, primary_key=True)
    city = db.Column('City', String(60), primary_key=True)
    block = db.Column('Block', Integer())
    address = db.Column('Address', String(100))
    lot = db.Column('Lot', String(15))
