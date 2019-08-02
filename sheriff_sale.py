import os
import json
import logging
import re
import requests
from datetime import datetime, date
from pathlib import Path
from utils import requests_content

from constants import SHERIFF_SALES_URL, SHERIFF_SALES_BASE_URL, SUFFIX_ABBREVATIONS, ADDRESS_REGEX_SPLIT, CITY_LIST


class SheriffSale:
    """
    Web scraper for sheriff sale website
    """

    def __init__(self):

        try:
            self.data = requests.get(SHERIFF_SALES_URL)
        except ConnectionError as err:
            raise ConnectionError("Cannot Access URL: ", err)

        self.session = requests.Session()
        self.soup = requests_content(SHERIFF_SALES_URL, self.session)

    def get_sale_dates(self):
        """
        Gathers all of sale dates available in the drop-down form
        """
        sale_dates = []
        for select in self.soup.find_all(name='select', attrs={'id': 'PropertyStatusDate'}):
<<<<<<< HEAD
            sale_dates = [option['value']
                          for option in select.find_all(name='option')[1:]]
=======
            sale_dates = [option['value'] for option in select.find_all(name='option')[1:]]
>>>>>>> master1

        return sale_dates

    def get_sale_links(self):
        """
        Gathers all of the href links for each listing and builds a list of all the links to each listing's details
        in the form of "https://salesweb.civilview.com/Sales/SaleDetails?PropertyId=563667001"
        """
        sale_links = []
        for row in self.soup.find_all('tr')[1:]:
            for link in row.find_all('a', href=True):
                sale_links.append(SHERIFF_SALES_BASE_URL + link['href'])

        return sale_links
<<<<<<< HEAD

    def get_property_ids(self):
=======

    def get_property_ids(self):
        """
        Gathers all the property id's from all of thge href links for each listing under details
        E.g. '563663246' from "/Sales/SaleDetails?PropertyId=563663246"
        """
        sale_links = self.get_sale_links()
        property_id = [re.findall('\d{9}', x)[0] for x in sale_links]

        return property_id

    def get_all_listing_details_tables(self):
        """
        Retrieves all table html data from each listings details. Run this once since its running several
        requests on hundreds of links.
        """
        sale_links = self.get_sale_links()
        listings_table_data = []
        for links in sale_links:
            html = requests_content(links, self.session)
            listings_table_data.append(html.find('div', class_='table-responsive'))

        return listings_table_data

    def get_table_data(self):
        listing_details_tables = self.get_all_listing_details_tables()
        table_data_html, status_history_html = [], []
        table_data, maps_url, status_history = [], [], []
        for listing in listing_details_tables:
            table_data_html.append(listing.find('table', class_='table table-striped'))
            status_history_html.append(listing.find('table', class_='table table-striped '))

        for table in table_data_html:
            table_data.append([x.text for x in table.find_all('td')[1::2]])
            for link in table.find_all('a', href=True):
                maps_url.append(link['href'])

        for status in status_history_html:
            status_history.append([x.text for x in status.find_all('td')])

        return table_data, maps_url, status_history

    def sanitize_address_data(self, table_data):
>>>>>>> master1
        """
        Gathers all the property id's from all of the href links for each listing under details
        E.g. '563663246' from "/Sales/SaleDetails?PropertyId=563663246"
        """
        sale_links = self.get_sale_links()
        property_id = [re.findall(r'\d{9}', x)[0] for x in sale_links]

        return property_id

    def get_sheriff_ids(self):
        """
        Gathers all the sheriff id's from the table_data
        'F-18001491'
        """
        sheriff_ids = []
        for row in self.soup.find_all('tr')[1:]:
            sheriff_ids.append(row.find_all('td')[1].text)

        return sheriff_ids

    def get_address_data(self):
        """Gathers all of the address data for each listing"""
        address_data = []
        for row in self.soup.find_all('tr')[1:]:
            for td in row.find_all('td')[5::5]:
                address_data.append(td.text)

<<<<<<< HEAD
        return address_data

    def get_all_listing_details_tables(self):
        """
        Retrieves all table html data from each listings details. Run this once since its running 
        several requests on hundreds of links.
        """
        sale_links = self.get_sale_links()
        listings_table_data = []
        for links in sale_links:
            html = requests_content(links, self.session)
            listings_table_data.append(
                html.find('div', class_='table-responsive'))
=======
        street_match = [re.search(regex_street, row).group(0).rstrip() for row in address_data]
        for key, value in SUFFIX_ABBREVATIONS.items():
            street_match = [re.sub(fr'({key})', value, row) for row in street_match]
>>>>>>> master1

        return listings_table_data

    def get_table_data(self):
        """
        Retrives data from each listing's detail page. Returns a list of table data,
        a google maps url, the status history.
        """
        listing_details_tables = self.get_all_listing_details_tables()

        table_data_html, status_history_html = [], []
        table_data, maps_url, status_history = [], [], []

        # Grabs all of the html for table data and status history
        for listing in listing_details_tables:
            table_data_html.append(listing.find(
                'table', class_='table table-striped'))
            status_history_html.append(listing.find(
                'table', class_='table table-striped '))

        # Parses html to grab the table data as well as the google maps url
        for table in table_data_html:
            table_data.append([x.text for x in table.find_all('td')[1::2]])
            for link in table.find_all('a', href=True):
                maps_url.append(link['href'])

        # Grabs the status history for each address
        for status in status_history_html:
            status_history.append([x.text for x in status.find_all('td')])

<<<<<<< HEAD
        return table_data, maps_url, status_history

    def sanitize_address_data(self):
=======
    # TODO: May deprecate since I'm gathering all data from site at once
    def selenium_driver(self, sale_date):
>>>>>>> master1
        """
        Returns lists of sanitized address data in the format of (Address, Unit, City, Zip Code)
        """
<<<<<<< HEAD
        regex_street = re.compile(
            r'.*?(?:' + r'|'.join(ADDRESS_REGEX_SPLIT) + r')\s')
        regex_city = re.compile(r'(' + '|'.join(CITY_LIST) + ') NJ')
        regex_unit = re.compile(r'(Unit|Apt.) ([0-9A-Za-z-]+)')
        regex_secondary_unit = re.compile(
            r'(Building|Estate) #?([0-9a-zA-Z]+)')
        regex_zip_code = re.compile(r'\d{5}')

        address_data = self.get_address_data()
=======
        driver = webdriver.Chrome()
        driver.get(SHERIFF_SALES_URL)
        driver.maximize_window()
>>>>>>> master1

        street_match, city_match = [], []

        try:
            street_match = [re.search(regex_street, row)
                            .group(0)
                            .rstrip() for row in address_data]

            # Cleanup: Remove any periods
            street_match = [re.sub(r'\.', '', row) for row in street_match]

        except AttributeError:
            street_match_check = [regex_street.findall(
                row) for row in address_data]
            for i, street in enumerate(street_match_check):
                if not street:
                    print('Street Error:', address_data[i])

<<<<<<< HEAD
        try:
            city_match = [re.search(regex_city, row).group(1)
                          for row in address_data]
        except AttributeError:
            city_match_check = [regex_city.findall(
                row) for row in address_data]
            for i, city in enumerate(city_match_check):
                if not city:
                    print('City Error:', address_data[i])

        unit_match = [re.search(regex_unit, row) for row in address_data]
        secondary_unit_match = [
            re.search(regex_secondary_unit, row) for row in address_data]
        zip_match = [re.search(regex_zip_code, row).group(0)
                     for row in address_data]

        # TODO: Do it only on the last word to avoid instances such as (1614 W Ave)
        # Abbreviates all street suffixes (e.g. Street, Avenue to St and Ave)
        for key, value in SUFFIX_ABBREVATIONS.items():
            street_match = [re.sub(fr'({key})', value, row)
                            for row in street_match]

        result = list(zip(street_match,
                          unit_match,
                          secondary_unit_match,
                          city_match,
                          zip_match
                          ))

        return result

    # def build_db(self, data, model, db):
    #     for d in data:
    #         _sheriff_sale_data = model(
    #             sheriff=d['listing_details']['sheriff'],
    #             court_case=d['listing_details']['court_case'],
    #             sale_date=d['listing_details']['sale_date'],
    #             plaintiff=d['listing_details']['plaintiff'],
    #             defendant=d['listing_details']['defendant'],
    #             address=d['listing_details']['address'],
    #             priors=d['listing_details']['priors'],
    #             attorney=d['listing_details']['attorney'],
    #             judgment=d['listing_details']['judgment'],
    #             deed=d['listing_details']['deed'],
    #             deed_address=d['listing_details']['deed_address'],
    #             address_sanitized=d['sanitized']['address'],
    #             unit=d['sanitized']['unit'],
    #             city=d['sanitized']['city'],
    #             zip_code=d['sanitized']['zip_code'],
    #             maps_href=d['maps_url']
    #         )
    #         return _sheriff_sale_data

=======
>>>>>>> master1
    def sheriff_sale_dict(self):
        """
        Structures all sheriff sale data in a list of dictionaries
        """
<<<<<<< HEAD

        property_id = self.get_property_ids()
        table_data = self.get_table_data()
        sanitized_table_data = self.sanitize_address_data()

        zipped = list(zip(property_id,
                          [x for x in table_data[0]],
                          sanitized_table_data,
                          table_data[1],
                          table_data[2]
                          ))

        list_dicts = []
        for data in zipped:
            _dict = {'property_id': data[0],
                     'listing_details': {
                         'sheriff': data[1][0],
                         'court_case': data[1][1],
                         'sale_date': datetime.strptime(data[1][2], '%m/%d/%Y').strftime('%m/%d/%Y'),
                         'plaintiff': data[1][3],
                         'defendant': data[1][4],
                         'address': data[1][5],
                         'priors': data[1][6],
                         'attorney': data[1][7],
                         'judgment': data[1][8],
                         'deed': data[1][9],
                         'deed_address': data[1][10]
            },
                'sanitized': {
                         'address': data[2][0],
                         'unit': data[2][1],
                         'secondary_unit': data[2][2],
                         'city': data[2][3],
                         'zip_code': data[2][4]
            },
                'maps_url': data[3],
                'status_history': data[4]
            }
            list_dicts.append(_dict)

        return list_dicts

    def json_dump(self, data):
        # Check if json_dumps directory exists and create it if it does not exist
        # TODO: Use pathlib instead
        current_dir = os.path.dirname(os.path.realpath(__file__))
        json_dumps_dir = f'{current_dir}\\json_dumps'

        if not os.path.exists(json_dumps_dir):
            os.makedirs(json_dumps_dir)

        # Create a json dump using the current date as the file name
        todays_date = date.today().strftime('%m_%d_%Y')
        json_dumps_path = Path(f"{json_dumps_dir}\\{todays_date}.json")

        if not json_dumps_path.exists():
            with open(f'{json_dumps_path}', 'w') as f:
                json.dump(data, f)

        return
=======

        property_id = self.get_property_ids()
        table_data = self.get_table_data()
        sanitized_table_data = self.sanitize_address_data(table_data[0])

        zipped = list(zip(property_id, [x for x in table_data[0]], sanitized_table_data,
                          table_data[1], table_data[2]))

        list_dicts = []
        for data in zipped:
            _dict = {'property_id': data[0],
                     'listing_details': {
                         'sheriff': data[1][0],
                         'court_case': data[1][1],
                         'sale_date': datetime.strptime(data[1][2], '%m/%d/%Y').strftime('%m/%d/%Y'),
                         'plaintiff': data[1][3],
                         'defendant': data[1][4],
                         'address': data[1][5],
                         'priors': data[1][6],
                         'attorney': data[1][7],
                         'judgment': data[1][8],
                         'deed': data[1][9],
                         'deed_address': data[1][10]
                     },
                     'sanitized': {
                         'address': data[2][0],
                         'unit': data[2][1],
                         'city': data[2][2],
                         'zip_code': data[2][3]
                     },
                     'maps_url': data[3],
                     'status_history': data[4]
                     }
            list_dicts.append(_dict)

        return list_dicts
>>>>>>> master1


if __name__ == "__main__":
    SHERIFF = SheriffSale()
<<<<<<< HEAD
    a = SHERIFF.sheriff_sale_dict()
=======
    # sale_date = sheriff.get_sale_dates()
    DATA = SHERIFF.sheriff_sale_dict()
    print(DATA)
>>>>>>> master1
