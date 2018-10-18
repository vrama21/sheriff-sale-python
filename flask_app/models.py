from flask_app import db
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table, DateTime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///site.db')
SourceSession = sessionmaker(engine)
metadata = MetaData()
metadata.reflect(engine)

Base = declarative_base()
Base.metadata.create_all(engine)

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


if __name__ == '__main__':

    SourceSession = sessionmaker(engine)

    dest_engine = create_engine('sqlite:///:memory:', echo=True)
    DestSession = sessionmaker(dest_engine)

    sourceSession = SourceSession()

    query = sourceSession.query(Pet.name, Pet.race).filter_by(race='cat')

    metadata = MetaData(bind=engine)
    columns = [Column(desc['name'], desc['type']) for desc in query.column_descriptions]
    column_names = [desc['name'] for desc in query.column_descriptions]
    table = Table("newtable", metadata, *columns)

    # Create the new table in the destination wdatabase
    table.create(engine)

    # Finally execute the query
    destSession = DestSession()
    for row in query:
        destSession.execute(table.insert(row))
    destSession.commit()