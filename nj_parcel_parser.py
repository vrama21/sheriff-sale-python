import requests
import re
import sqlite3
import json
from sheriff_sale import SheriffSale
from collections import OrderedDict, defaultdict
from bs4 import BeautifulSoup
from constants import *


def requests_content(url):
    html_data = requests.get(url)
    content = html_data.content
    soup = BeautifulSoup(content, 'html.parser')
    return soup


class ParseNJParcels:

    def __init__(self, county=None, city=None):
        self.soup = requests_content(nj_parcels_url)

        self.city_num_dict = {}
        self.main_dict = defaultdict(dict)

        self.county = county
        self.city = city
        self.sheriff_sale_list = SheriffSale()
        print(self.sheriff_sale_list)

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
        city_list = self.main_dict[self.county]

        _soup = requests_content(nj_parcels_url + self.city_num_dict[str(self.city)])

        table_data = _soup.find('table', class_='table')
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
            _url = nj_parcels_url + self.city_num_dict[str(self.city)] + '/' + block
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


if __name__ == '__main__':
    main = ParseNJParcels(county='Atlantic County')
    main.build_main_dict()
    # main.build_database()
    # main.build_block_list()
    # main.build_address_list()

