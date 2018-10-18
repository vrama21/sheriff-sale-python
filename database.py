from base import engine, Session, Base
from database_models import SheriffSaleDB, NJParcelsDB
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError
from sheriff_sale import SheriffSale

# TODO: Remove db_model parameter and specify by model class name


class Database:

    def __init__(self, db_model):
        self.db_model = db_model
        self.engine = engine

    def query_db(self, db_field, db_value):
        query = Session.query(self.db_model).filter(db_field == db_value)
        result = Session.execute(query)
        data_rows = result.fetchall()

        return data_rows

    def check_if_value_exists(self, db_field, db_value):
        row_exists = Session.query(self.db_model).filter(db_field == db_value).first()
        if row_exists:
            return True
        else:
            return False

    def sheriff_sale_append(self, sale_date):
        db = SheriffSaleDB()
        sheriff_sale = SheriffSale()
        sheriff_sale_table_data = sheriff_sale.selenium_driver(sale_date)
        zipped_data = sheriff_sale.sheriff_sale_zipped(sheriff_sale_table_data)

        try:
            for _val in zipped_data:
                db.sheriff = _val[0]
                db.sale_date = _val[1]
                db.plaintiff = _val[2]
                db.defendant = _val[3]
                db.address = _val[4]
                row = (SheriffSaleDB(sheriff=db.sheriff,
                                     sale_date=db.sale_date,
                                     plaintiff=db.plaintiff,
                                     defendant=db.defendant,
                                     address=db.address))
                # Only appends addresses that do not exist in the database
                row_exists = Session.query(exists().where(SheriffSaleDB.address == _val[4])).scalar()
                if not row_exists:
                    Session.add(row)
            Session.commit()
        except SQLAlchemyError as e:
            print(e)
        finally:
            Session.close()


if __name__ == '__main__':
    db = Database('nj_parcels.db', NJParcelsDB)
    a = db.query_db(NJParcelsDB.address, '122 REEDS RD')
    b = db.check_if_value_exists(NJParcelsDB.address, '122 REEDS RD')
    # db = Database('sheriff_sale.db')
    # a = db.query_db(SheriffSaleDB, SheriffSaleDB.sale_date, '8/9/2018')
    print(a)
    print(b)

