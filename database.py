import sqlite3
import requests
import json
import pprint
from constants import *
from nj_parcel_parser import ParseNJParcels


class ParseDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('nj_parcels.db')
        self.cur = self.conn.cursor()

        parse = ParseNJParcels()
        self.dict_keys = parse.main_dict.keys()

    def build_database(self):
        with self.conn:

            county_list = self.dict_keys
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
        _address = list()
        _address.append(address)

        if type(address) is list:
            _address = _address.pop(0)
            _address = [x.upper() for x in _address]
            _address = tuple(_address)
            query = """
                SELECT *
                FROM Atlantic
                WHERE Address IN {}
                """.format(_address)
            self.cur.execute(query)

        elif type(address) is str:
            _address = [''.join(x.upper()) for x in _address]
            _address = _address.pop(0)

            query = """
                SELECT *
                FROM Atlantic
                WHERE Address = (?)
                """

            self.cur.execute(query, [_address])

        _data = self.cur.fetchall()

        return _data

    def parse_json_url(self, parsed_data):
        selected_data = parsed_data
        city_num_json = json.load(open('city_nums.json'))
        json_full = []
        json_prop = []

        if len(selected_data) > 1:
            for i in selected_data:
                city_num = city_num_json[i[0]]

                url = nj_parcels_api_url + '{}_{}_{}.json'.format(city_num, i[1], i[3])
                resp = requests.get(url)
                _json = resp.json()
                json_full.append(_json)
        else:
            try:
                city_num = city_num_json[selected_data[0][0]]
                url = nj_parcels_api_url + '{}_{}_{}.json'.format(city_num, selected_data[0][1], selected_data[0][3])
                resp = requests.get(url)
                _json = resp.json()
                json_full.append(_json)
            except IndexError:
                print('Error: Address could not be located in the database')

        for j in json_full:
            index = json_full.index(j)
            json_prop.append(json_full[index]['features'][0]['properties'])

        return json_prop


if __name__ == '__main__':
    data = ParseDatabase()
    selected = data.select_data(county='Atlantic', address=['122 Reeds Rd', '856 N New Rd', '82 E Washington Ave'])
    # selected = data.select_data(county='Atlantic', address='122 Reeds Rd')
    json = data.parse_json_url(selected)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(json)
