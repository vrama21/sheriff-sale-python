import json
import re
import requests
import sqlite3
from sheriff_sale import SheriffSale
from collections import defaultdict
from constants import *
from utils import requests_content
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from database_models import Base


class ParseNJParcels:
    """
    Web scraper for www.njparcels.com
    """
    def __init__(self, county=None, city=None):
        self.soup = requests_content(NJ_PARCELS_URL)

        self.city_num_dict = {}
        self.main_dict = defaultdict(dict)

        self.county = county
        self.city = city
        self.sheriff_sale_list = SheriffSale()

    def build_main_dict(self):
        div_html = self.soup.find('div', class_='col-md-12')
        div_child = div_html.find('div')

        city_names = []
        city_nums = []
        county_name = None

        for i in div_child:
            if i.name == 'h2':
                county_name = i.get_text()
            if i.name == 'span':
                city_name = i.get_text()
                city_names.append(city_name)
                city_num = re.findall('/property/(.+)/"', str(i))
                for num in city_num:
                    city_num = ''.join(num)
                    city_nums.append(city_num)
                # self.main_dict[county_name] = city_name
                self.main_dict[county_name].update({city_name: {}})

        with open('city_nums.json', 'w') as fp:
            self.city_num_dict = {key: value for (key, value) in zip(city_names, city_nums)}
            json.dump(self.city_num_dict, fp)

    def build_block_list(self):
        soup = requests_content(NJ_PARCELS_URL + self.city_num_dict[str(self.city)])

        table_data = soup.find('table', class_='table')
        block_num_data = table_data.find_all('a', href=True)
        block_num_text = [x.get_text() for x in block_num_data]

        regex = r'(\d+(\.\d*)?)'
        a = re.findall(regex, str(block_num_text))
        block_nums = [x[0] for x in a]

        self.main_dict[self.county][self.city] = block_nums
        # self.main_dict[self.county][city].update({block_nums: {}})

    def build_address_list(self):
        conn = sqlite3.connect('nj_parcels.db')
        cur = conn.cursor()

        block_num = self.main_dict[self.county][self.city]

        for block in block_num:
            _url = NJ_PARCELS_URL + self.city_num_dict[str(self.city)] + '/' + block
            _soup = requests_content(_url)
            print(_url)

            addr_data = _soup.find_all('td')[1::4]
            addr_text = [x.get_text() for x in addr_data]

            lot_num_data = _soup.find_all('a', href=True)
            lot_num_data = lot_num_data[6:]
            lot_num_text = [x.get_text() for x in lot_num_data]

            addr_lot_zip = [x for x in zip(addr_text, lot_num_text)]

            block_index = block_num.index(block)
            self.main_dict[self.county][self.city][block_index] = addr_lot_zip

            for addr in addr_lot_zip:
                cur.execute("""INSERT INTO AtlanticCounty (City, Block, Address, Lot)
                            VALUES (?, ?, ?, ?)""",
                            (self.city, block, addr[0], addr[1]))

                conn.commit()

    def parse_json_url(self, parsed_data):
        # city_num_json = json.load(open('city_nums.json'))
        with open('city_nums.json') as json_file:
            json_full = []
            json_prop = []

            if len(parsed_data) > 1:
                for i in parsed_data:
                    city_num = json_file[i[0]]

                    url = NJ_PARCELS_API + f'{city_num}_{i[1]}_{i[3]}.json'
                    resp = requests.get(url)
                    json_data = resp.json()
                    json_full.append(json_data)
            else:
                try:
                    city_num = json_file[parsed_data[0][0]]
                    url = NJ_PARCELS_API + f'{city_num}_{parsed_data[0][1]}_{parsed_data[0][3]}.json'
                    resp = requests.get(url)
                    json_data = resp.json()
                    json_full.append(json_data)
                except IndexError:
                    print('Error: Address could not be located in the database')

            for j in json_full:
                index = json_full.index(j)
                json_prop.append(json_full[index]['features'][0]['properties'])

            return json_prop


if __name__ == '__main__':
    main = ParseNJParcels(county='Atlantic County')
    main.build_main_dict()
    # main.build_database()
    # main.build_block_list()
    # main.build_address_list()

