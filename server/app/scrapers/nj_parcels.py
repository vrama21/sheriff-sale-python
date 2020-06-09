from collections import defaultdict
import json
import logging
import re
import requests
from ..constants import NJ_PARCELS_URL, NJ_PARCELS_API
from ..utils import requests_content, load_json_data


class NJParcels:
    """
    Web scraper for www.njparcels.com
    """
    def __init__(self, county=None, city=None):
        self.session = requests.Session()
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

    def get_property_parameters(self, address):
        """
        Gets links to the specified address info, comparables, and previous sales.
        Also gets the city, block, and lot numbers of the specified address.
        """
        format_address = "+".join(address.split())
        NJ_PARCELS_SEARCH_URL = f"http://njparcels.com/search/address/?s={format_address}&s_co=%23%23"
        request = requests_content(NJ_PARCELS_SEARCH_URL)

        try:
            results_html = request.find('div', class_="btn-group-vertical")
            property_links_html = results_html.find_all('a', href=True)
            property_links = [link['href'] for link in property_links_html]

            city_block_lot = property_links[1].split('/')[-1]
            return {
                'links': {
                    'info': property_links[0],
                    'sales': property_links[1],
                    'comparables': property_links[2]
                },
                'cityBlockLot': city_block_lot
            }
        except AttributeError as error:
            logging.error(f'{error}. There were no NJ Parcels Search Results for {address}')

    def get_property_taxes(self, city_block_lot):
        """
        Gets the taxes for the specified property
        """
        url = f"{NJ_PARCELS_API}/{city_block_lot}.json"
        request = requests.get(url).json()
        property_values = request['features'][0]['properties']

        return {
            'taxes': property_values['taxes']
        }
