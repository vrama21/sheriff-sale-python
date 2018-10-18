import sqlite3
import requests
import json
from constants import NJ_PARCELS_API
from nj_parcel_parser import ParseNJParcels


class Database:

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def build_database(self):
        parse = ParseNJParcels()
        dict_keys = parse.main_dict.keys()

        with self.conn:

            county_list = dict_keys
            county_list = [''.join(x.split()) for x in county_list]

            command = """
                      CREATE TABLE ? (
                      City text,
                      Block text,
                      Address text,
                      Lot text
                      )"""
            try:
                for county in county_list:
                    self.cur.execute(command, county)
            except sqlite3.OperationalError:
                pass

            self.conn.commit()
            self.conn.close()

    def select_data(self, county, address):
        _address = address
        placeholder = '?'
        placeholders = ', '.join(placeholder for unused in _address)
        query = f"""
            SELECT *
            FROM {county}
            WHERE Address IN ({placeholders})
            """
        self.cur.execute(query, _address)
        _data = self.cur.fetchall()

        return _data




if __name__ == '__main__':
    data = Database()
    a = data.select_data(county='Atlantic', address=['122 Reeds Rd', '856 N New Rd'])
