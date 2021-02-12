import json

import re
import requests
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote

from . import match_parser, error_handler
from ...constants import (
    ADDRESS_REGEX_SPLIT,
    CITY_LIST,
    COUNTY_MAP,
    NJ_DATA,
    SHERIFF_SALES_BASE_URL,
    SHERIFF_SALES_URL,
    SUFFIX_ABBREVATIONS,
)
from ...utils import load_json_data, requests_content


class SheriffSale:
    """
    Web scraper for sheriff sale website
    """

    def __init__(self, county=None):

        self.county_name = county
        self.county_id = self.county_name and self.get_sheriff_sale_county_id(self.county_name)

        try:
            self.session = requests.Session()
            self.soup = requests_content(f"{SHERIFF_SALES_URL}{self.county_id}", self.session)
        except ConnectionError as err:
            raise ConnectionError("Cannot Access URL: ", err)

        self.table_div = self.soup.find("table", class_="table table-striped")

        error_handler(self.table_div, 'The Sheriff Sale Table Div was not captured')

    def get_sheriff_sale_county_id(self, county):
        nj_json_data = load_json_data('data/NJ_Data.json')
        sheriff_sale_county_id = nj_json_data[county]['sheriffSaleId']

        return sheriff_sale_county_id

    def get_sale_dates(self):
        """
        Gathers all of sale dates available in the drop-down form
        """
        sale_dates = []
        for select in self.soup.find_all(name="select", attrs={"id": "PropertyStatusDate"}):
            sale_dates = [option["value"] for option in select.find_all(name="option")[1:]]

        return sale_dates

    def get_listings_details_links(self):
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
        sale_links = self.get_listings_details_links()
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
        sale_links = self.get_listings_details_links()

        listings_table_data = []

        for links in sale_links:
            request = requests_content(links, self.session)
            property_id = re.search(r'\d{9}', links).group(0)
            html = request.find("div", class_="table-responsive")

            listings_table_data.append({"propertyId": property_id, "html": html})

        return listings_table_data

    def main(self):
        """
        Gathers all of the listings for a specified county and returns it in a dictionary
        """
        listing_details_tables = self.get_all_listing_details_tables()

        table_data = []
        for listing in listing_details_tables:
            listing_html = listing['html'].find("table", class_="table table-striped")
            status_history_html = listing['html'].find("table", id="longTable")
            maps_url = listing_html.find("a", href=True)

            listing_table_data = [x.text.strip().title() for x in listing_html.find_all("td")[1::3]]

            address_br = listing['html'].find("br")
            address = f'{address_br.previous_element} {address_br.next_element}'.strip().title()

            address_sanitized = self.sanitize_address(address)

            status_history = []
            for row in status_history_html.find_all("tr")[1:]:
                td = row.find_all("td")
                listing_status = {
                    'status': td[0].text.strip(),
                    'date': td[1].text.strip(),
                }
                status_history.append(listing_status)

            listing_table_dict = {
                "address": address,
                "attorney": listing_table_data[8],
                "attorney_phone": listing_table_data[9],
                "city": address_sanitized['city'],
                "county": address_sanitized['county'],
                "court_case": listing_table_data[2],
                "defendant": listing_table_data[5],
                "judgment": listing_table_data[1],
                "maps_url": maps_url and maps_url['href'],
                "parcel": listing_table_data[6],
                "plaintiff": listing_table_data[4],
                "sale_date": listing_table_data[3],
                "sheriff": listing_table_data[0],
                "zip_code": address_sanitized['zip_code'],
            }

            table_data.append(listing_table_dict)

        return table_data
