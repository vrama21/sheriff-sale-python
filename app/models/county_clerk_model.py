from .. import db


class CountyClerk(db.Model):
    __tablename__ = 'county_clerk'
    __table_args__ = {'extend_existing': True}

    id = db.Column('id', db.Integer, primary_key=True)
    doc_id = db.Column('doc_id', db.Integer, unique=True)
    rowid = db.Column('rowid', db.Integer)

    block = db.Column('block', db.String)
    book = db.Column('book', db.Integer)
    correction_flag = db.Column('correction_flag', db.String)
    cross_party_name = db.Column('cross_party_name', db.String)
    doc_status = db.Column('doc_status', db.String)
    doc_type = db.Column('doc_type', db.String)
    file_num = db.Column('file_num', db.String)
    legal_1 = db.Column('legal_1', db.String)
    lot = db.Column('lot', db.String)
    page = db.Column('page', db.Integer)
    party_code = db.Column('party_code', db.String)
    party_name = db.Column('party_name', db.String)
    pv_no_data = db.Column('pv_no_data', db.String)
    rec_date = db.Column('rec_date', db.String)
    town = db.Column('town', db.String)

    @property
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
