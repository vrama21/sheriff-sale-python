import logging
import re
from typing import Literal, Union
from bs4 import BeautifulSoup

import requests

from app.utils import load_json_data, requests_content

from .sheriff_sale_listing import SheriffSaleListing
from .sheriff_sale_status_history import SheriffSaleStatusHistory


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
        cookies = {'ASP.NET_SessionId': 'swrddrsjkdy4yq5vskb42w22'}
        payload = {'countyId': self.county_id, 'isOpen': filter_out_sold_listings}

        self.soup = requests_content(
            url=sheriff_sale_url,
            method='POST',
            cookies=cookies,
            data=payload,
            session=self.session,
        )
        self.table_div = self.soup.find('table', class_='table table-striped')

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
        request = requests_content(url=sheriff_sales_url, method='GET')

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
            property_id = re.search(r'\d{9}', table_row[0].find('a', href=True)['href']).group(0)
            data = {
                'property_id': property_id,
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

        if self.listings is None:
            self.get_all_listings()

        property_ids = [int(listing['property_id']) for listing in self.listings]

        return property_ids

    def get_all_listing_sheriff_ids(self) -> list:
        """
        Gathers all the sheriff id's from the table_data
        'F-18001491'
        """

        if self.listings is None:
            self.get_all_listings()

        sheriff_ids = [listing['sheriff_id'] for listing in self.listings]

        return sheriff_ids

    def get_all_listing_address(self) -> list:
        """
        Gathers all of the address data for each listing
        """
        if self.listings is None:
            self.get_all_listings()

        addresses = [listing['address'] for listing in self.listings]

        return addresses

    def get_all_listing_sale_dates(self) -> list:
        """
        Gathers all of the sale date for each listing
        """
        if self.listings is None:
            self.get_all_listings()

        sale_dates = [listing['sale_date'] for listing in self.listings]
        sale_dates = list(set(sale_dates))

        return sale_dates

    def get_listing_details(self, property_id: str):
        """
        Gathers all table html data from each listings details.
        """
        if self.listings is None:
            self.get_all_listings()

        listings_table_data = []

        for links in self.sale_links:
            request = requests_content(links, self.session)
            html = request.find('div', class_='table-responsive')

            listings_table_data.append(html)

        return listings_table_data

    def get_new_listing_details_html(self, property_id) -> Union[BeautifulSoup, None]:
        """
        Gathers all table html data from listings that do not exist within the database yet.
        """
        listing_details_url = f'https://salesweb.civilview.com/Sales/SaleDetails?PropertyId={property_id}'
        listing_details_html = requests_content(url=listing_details_url, method='GET', session=self.session)

        return listing_details_html

    def get_listing_details_and_status_history(self, use_google_map_api: bool) -> list:
        property_ids = self.get_all_listing_property_ids()

        all_listings = []
        for property_id in property_ids:
            listing_soup = self.get_new_listing_details_html(property_id)

            if listing_soup:
                listing = SheriffSaleListing(
                    county=self.county_name, listing_html=listing_soup, property_id=property_id
                ).parse(use_google_map_api)
                status_history = SheriffSaleStatusHistory(listing_html=listing_soup, property_id=property_id).parse()

                all_listings.append({'listing': listing, 'status_history': status_history})

        return all_listings
