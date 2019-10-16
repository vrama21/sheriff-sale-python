from collections import defaultdict
import json
import re
import requests
from constants import NJ_PARCELS_URL, NJ_PARCELS_API
from utils import requests_content


class NJParcels:
    """
    Web scraper for www.njparcels.com
    """
    def __init__(self, county=None, city=None):
        self.session = requests.session()
        self.soup = requests_content(NJ_PARCELS_URL, self.session)

        self.county = county
        self.city = city

        self.city_num_dict = {}
        self.main_dict = defaultdict(dict)

    def get_county_list(self):
        """ Returns a list of all the available counties """
        county_list = [x.text for x in self.soup.find_all('h2', class_='countyname')]
        return county_list

    def get_city_list(self):
        """ Returns a list of all the available cities """
        city_list = [x.text for x in self.soup.find_all('span', class_='muniname')]
        return city_list

    def get_city_num_list(self):
        """ Returns a list of the numbers used for each city (E.g. Absecon is 0101) """
        div = self.soup.find('div', class_='col-md-12')
        find_all_nums = [re.findall(r'\d{4}', x['href']) for x in div.find_all('a', href=True)]
        city_num_list = [x[0] for x in find_all_nums[3:]]
        return city_num_list

    def write_city_nums_json(self):
        """ Writes a json file with each city and their respective city number
        (E.g. Atlantic City: 0102) """

        with open('city_nums.json', 'w') as file_path:
            city_num_dict = {county: {city: num} for (county, city, num) in zip(county_names, city_names, city_nums)}
            json.dump(city_num_dict, file_path)

    def build_block_list(self):
        soup = requests_content(f'{NJ_PARCELS_URL}{self.city_num_dict[str(self.city)]}')

        table_data = soup.find('table', class_='table')
        block_num_data = table_data.find_all('a', href=True)
        block_num_text = [x.get_text() for x in block_num_data]

        regex = re.compile(r'(\d+(\.\d*)?)')
        a = re.findall(regex, str(block_num_text))
        block_nums = [x[0] for x in a]

        self.main_dict[self.county][self.city] = block_nums
        # self.main_dict[self.county][city].update({block_nums: {}})

    def build_address_list(self):
        block_num = self.main_dict[self.county][self.city]

        for i, block in enumerate(block_num):
            _url = NJ_PARCELS_URL + self.city_num_dict[str(self.city)] + '/' + block
            _soup = requests_content(_url)
            print(_url)

            addr_data = _soup.find_all('td')[1::4]
            addr_text = [x.get_text() for x in addr_data]

            lot_num_data = _soup.find_all('a', href=True)
            lot_num_data = lot_num_data[6:]
            lot_num_text = [x.get_text() for x in lot_num_data]

            addr_lot_zip = [x for x in zip(addr_text, lot_num_text)]

            self.main_dict[self.county][self.city][i] = addr_lot_zip

    def parse_json_url(self, parsed_data):
        with open('city_nums.json') as json_file:
            json_full = []
            json_prop = []

            print(parsed_data)
            if len(parsed_data) > 1:
                for i in parsed_data:
                    city_num = json_file[i[0]]

                    url = f'{NJ_PARCELS_API}{city_num}_{i[1]}_{i[3]}.json'
                    resp = requests.get(url).json()
                    json_full.append(resp)
            else:
                try:
                    city_num = json_file[parsed_data[0][0]]
                    url = f'{NJ_PARCELS_API}{city_num}_{parsed_data[0][1]}_{parsed_data[0][3]}.json'
                    resp = requests.get(url).json()
                    json_full.append(resp)
                except IndexError:
                    print('Error: Address could not be located in the database')

            for j in json_full:
                index = json_full.index(j)
                json_prop.append(json_full[index]['features'][0]['properties'])

            return json_prop

if __name__ == '__main__':
    main = NJParcels(county='Atlantic County')
    main.parse_json_url()