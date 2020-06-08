import json
import logging
import re
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote

import requests
from ..constants import (
    ADDRESS_REGEX_SPLIT,
    CITY_LIST,
    COUNTY_MAP,
    NJ_DATA,
    SHERIFF_SALES_BASE_URL,
    SHERIFF_SALES_URL,
    SUFFIX_ABBREVATIONS,
)
from ..utils import load_json_data, requests_content, match_parser
from ..settings import BASE_DIR


class SheriffSale:
    """
    Web scraper for sheriff sale website
    """
    def __init__(self, county=None):
        try:
            self.data = requests.get(SHERIFF_SALES_URL)
        except ConnectionError as err:
            raise ConnectionError("Cannot Access URL: ", err)

        self.county_name = list(county.keys())[0]
        self.county_id = county.get(self.county_name)

        self.session = requests.Session()

        self.soup = requests_content(f"{SHERIFF_SALES_URL}{self.county_id}", self.session)

        self.table_div = self.soup.find("table", class_="table table-striped")
        if not self.table_div:
            logging.error('The Sheriff Sale Table Div was not captured')

    def get_sale_dates(self):
        """
        Gathers all of sale dates available in the drop-down form
        """
        sale_dates = []
        for select in self.soup.find_all(name="select", attrs={"id": "PropertyStatusDate"}):
            sale_dates = [option["value"] for option in select.find_all(name="option")[1:]]

        sale_dates = [x.replace("/", "-") for x in sale_dates]

        return sale_dates

    def get_sale_links(self):
        """
        Gathers all of the href links for each listing and builds a list of all the links to each listing's details
        in the form of "https://salesweb.civilview.com/Sales/SaleDetails?PropertyId=563667001"
        """
        sale_links = []
        for row in self.soup.find_all("td", attrs={"class": "hidden-print"}):
            for link in row.find_all("a", href=True):
                sale_links.append(SHERIFF_SALES_BASE_URL + link["href"])

        return sale_links

    def get_property_ids(self):
        """
        Gathers all the property id's from all of the href links for each listing under details
        E.g. '563663246' from "/Sales/SaleDetails?PropertyId=563663246"
        """
        sale_links = self.get_sale_links()
        property_ids = [re.findall(r"\d{9}", x)[0] for x in sale_links]

        return property_ids

    def get_sheriff_ids(self):
        """
        Gathers all the sheriff id's from the table_data
        'F-18001491'
        """

        sheriff_ids = []
        for row in self.table_div.find_all("tr")[1:]:
            sheriff_ids.append(row.find_all("td")[1].text)

        return sheriff_ids

    def get_address_data(self):
        """
        Gathers all of the address data for each listing
        """

        address_data = []
        for row in self.soup.find_all("tr")[1:]:
            for td in row.find_all("td")[5::5]:
                address_data.append(td.text)

        return address_data

    def get_all_listing_details_tables(self):
        """
        Retrieves all table html data from each listings details.
        """
        sale_links = self.get_sale_links()

        listings_table_data = []

        for links in sale_links:
            request = requests_content(links, self.session)
            property_id = re.search(r'\d{9}', links).group(0)
            html = request.find("div", class_="table-responsive")

            listings_table_data.append({"propertyId": property_id, "html": html})

        return listings_table_data

    def sanitize_address(self, address):
        """
        Returns lists of sanitized address data in the format of { address, city, unit, secondary_unit, zip_code }
        """
        regex_street = re.compile(r".*?(?:" + r"|".join(ADDRESS_REGEX_SPLIT) + r")\s")
        regex_city = re.compile(r"(" + "|".join(CITY_LIST) + ") (NJ|Nj)")
        regex_unit = re.compile(r"(Unit|Apt).([0-9A-Za-z-]+)")
        regex_secondary_unit = re.compile(r"(Building|Estate) #?([0-9a-zA-Z]+)")
        regex_zip_code = re.compile(r"\d{5}")

        results = []

        street_match = match_parser(regex_street, address)
        city_match = match_parser(regex_city, address, regexGroup=1)
        unit_match = match_parser(regex_unit, address, log=False)
        secondary_unit_match = match_parser(regex_secondary_unit, address, log=False)
        zip_code_match = match_parser(regex_zip_code, address, log=False)

        try:
            for key, value in SUFFIX_ABBREVATIONS.items():
                re.sub(key, value, street_match)
        except TypeError:
            pass

        return {
            'street': street_match,
            'city': city_match,
            'zipCode': zip_code_match,
            'unit': unit_match,
            'unitSecondary': secondary_unit_match
        }

    def get_table_data(self):
        """
        Gathers all of the listings for a specified county and returns it in a dictionary
        """
        listing_details_tables = self.get_all_listing_details_tables()

        listing_keys = [
            'sheriff', 'courtCase', 'saleDate', 'plaintiff', 'defendant', 'address', 'priors', 'attorney', 'judgement',
            'deed', 'deedAddress'
        ]
        status_history_keys = ['status', 'date']

        table_data = []
        for listing in listing_details_tables:
            listing_html = listing['html'].find("table", class_="table table-striped")
            status_history_html = listing['html'].find("table", id="longTable")
            maps_url = listing_html.find("a", href=True)

            listing_table_data = [x.text.strip().title() for x in listing_html.find_all("td")[1::3]]

            address_br = listing['html'].find("br")
            address = f'{address_br.previous_element} {address_br.next_element}'.strip().title()

            status_history = []
            for row in status_history_html.find_all("tr")[1:]:
                td = row.find_all("td")
                listing_status = {
                    'status': td[0].text.strip(),
                    'date': td[1].text.strip(),
                }
                status_history.append(listing_status)

            listing_table_dict = dict(zip(listing_keys, listing_table_data))
            listing_table_dict['address'] = address
            listing_table_dict['addressSanitized'] = self.sanitize_address(listing_table_dict['address'])
            listing_table_dict['propertyId'] = listing['propertyId']
            listing_table_dict['statusHistory'] = status_history

            try:
                listing_table_dict['maps'] = maps_url["href"]
            except TypeError as error:
                listing_table_dict['maps'] = None

            table_data.append(listing_table_dict)

        return table_data
