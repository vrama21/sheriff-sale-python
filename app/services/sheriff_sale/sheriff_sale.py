import logging
import re
from typing import TypedDict, Union
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

from app.utils import load_json_data, requests_content

from .sheriff_sale_listing import SheriffSaleListing
from .sheriff_sale_status_history import SheriffSaleStatusHistory


class ParsedListingType(TypedDict):
    listing: SheriffSaleListing
    status_history: list[SheriffSaleStatusHistory]


class SheriffSale:
    """
    Web scraper for sheriff sale website

    :param county:

    """

    def __init__(self, county: str, filter_out_sold_listings: bool = True):
        self.county_name = county
        self.county_id = self.get_sheriff_sale_county_id()
        self.session = requests.Session()

        sheriff_sale_url = 'https://salesweb.civilview.com/Sales/SalesSearch?'
        query_params = {'countyId': self.county_id}
        sheriff_sale_request_url = sheriff_sale_url + urlencode(query_params)

        self.soup = requests_content(
            url=sheriff_sale_request_url,
            session=self.session,
        )

        self.table_div = self.soup.find_all('table')[-1]

        self.sale_links: Union[list[str], None] = None
        self.listings: Union[list[dict[str, any]], None] = None

    def get_sheriff_sale_county_id(self) -> str:
        nj_json_data = load_json_data('data/NJ_Data.json')
        sheriff_sale_county_id = nj_json_data[self.county_name]['sheriffSaleId']

        return sheriff_sale_county_id

    def get_counties(self) -> list:
        """
        Gathers all counties that are listed on the sheriff sale website
        """
        sheriff_sales_url = 'https://salesweb.civilview.com/'
        request = requests_content(url=sheriff_sales_url)

        trs = [x.text.strip().split() for x in request.find_all('tr')]
        counties = [tr[0] for tr in trs if tr[-1] == 'NJ']

        return counties

    def get_all_listings(self) -> list:
        """
        Gathers all aggregate listings on the initial county view
        """
        if not self.table_div:
            logging.error(f'The Sheriff Sale Table Div for {self.county_name} County was not captured')
            return

        listings = []
        table_rows = [table_row.find_all('td') for table_row in self.table_div.find_all('tr')[1:]]

        for table_row in table_rows:
            details_href = table_row[0].find('a', href=True)['href']
            property_id_search = re.search(r'\d+', details_href)

            data = {
                'property_id': property_id_search.group(0),
                'sheriff_id': table_row[1].text,
                'sale_date': table_row[2].text,
                'address': table_row[5].text,
            }
            listings.append(data)

        self.listings = listings

        return self.listings

    def get_all_listing_property_ids(self) -> list:
        """
        Gathers all of the property ids for each listing
        """
        if not self.table_div:
            logging.error(f'The Sheriff Sale Table Div for {self.county_name} County was not captured')
            return []

        if not self.listings:
            self.get_all_listings()

        property_ids = [int(listing['property_id']) for listing in self.listings]

        return property_ids

    def get_all_listing_sheriff_ids(self) -> list:
        """
        Gathers all the sheriff id's from the table_data
        'F-18001491'
        """

        if not self.listings:
            self.get_all_listings()

        sheriff_ids = [listing['sheriff_id'] for listing in self.listings]

        return sheriff_ids

    def get_all_listing_address(self) -> list:
        """
        Gathers all of the address data for each listing
        """
        if not self.listings:
            self.get_all_listings()

        addresses = [listing['address'] for listing in self.listings]

        return addresses

    def get_all_listing_sale_dates(self) -> list:
        """
        Gathers all of the sale date for each listing
        """
        if not self.listings:
            self.get_all_listings()

        sale_dates = [listing['sale_date'] for listing in self.listings]
        sale_dates = list(set(sale_dates))

        return sale_dates

    def parse_listing_details_html(self, property_id) -> Union[BeautifulSoup, None]:
        """
        Gathers all table html data from listings that do not exist within the database yet.
        """
        query_params = {'PropertyId': property_id}
        listing_details_url = 'https://salesweb.civilview.com/Sales/SaleDetails?' + urlencode(query_params)
        listing_details_html = requests_content(url=listing_details_url, session=self.session)

        return listing_details_html

    def get_listing_details_and_status_history(self, use_google_map_api: bool) -> list[ParsedListingType]:
        property_ids = self.get_all_listing_property_ids()

        all_listings = []
        for property_id in property_ids:
            listing_html = self.parse_listing_details_html(property_id)

            if listing_html:
                listing = SheriffSaleListing(
                    county=self.county_name, listing_html=listing_html, property_id=property_id
                ).parse(use_google_map_api)
                status_history = SheriffSaleStatusHistory(listing_html=listing_html, property_id=property_id).parse()

                all_listings.append({'listing': listing, 'status_history': status_history})

        return all_listings
