import logging
import re
import requests
from typing import List

from app import db
from app.utils import requests_content, load_json_data
from .sheriff_sale_listing import SheriffSaleListing
from .sheriff_sale_status_history import SheriffSaleStatusHistory
from app.models import Listing


class SheriffSale:
    """
    Web scraper for sheriff sale website

    :param county:

    """

    def __init__(self, county: str):

        self.county_name = county
        self.county_id = self.get_sheriff_sale_county_id(county=self.county_name)
        self.session = requests.Session()

        sheriff_sale_county_url = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=' + self.county_id

        self.soup = requests_content(sheriff_sale_county_url, self.session)
        self.table_div = self.soup.find('table', class_='table table-striped')

        self.sale_links = None
        self.listings = None

    def get_sheriff_sale_county_id(self, county):
        nj_json_data = load_json_data('data/NJ_Data.json')
        sheriff_sale_county_id = nj_json_data[county]['sheriffSaleId']

        return sheriff_sale_county_id

    def get_counties(self):
        """
        Gathers all counties that are listed on the sheriff sale website
        """
        sheriff_sales_url = 'https://salesweb.civilview.com/'
        request = requests_content(sheriff_sales_url)

        trs = [x.text.strip().split() for x in request.find_all('tr')]
        counties = [tr[0] for tr in trs if tr[-1] == 'NJ']

        return counties

    def get_listings_details_links(self):
        """
        Gathers all of the href links for each listing and builds a list of all the links to each listing's details
        in the form of 'https://salesweb.civilview.com/Sales/SaleDetails?PropertyId=563667001'
        """
        table_rows = [table_row.find_all('td')[0] for table_row in self.table_div.find_all('tr')[1:]]
        sale_links = [table_row.find('a', href=True)['href'] for table_row in table_rows]
        print(sale_links)

        # for row in self.table_div.find_all('td', attrs={'class': 'hidden-print'}):
        #     for link in row.find_all('a', href=True):
        #         sale_links.append('https://salesweb.civilview.com' + link['href'])

        self.sale_links = sale_links

    def get_all_listings(self):
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

    def get_all_listing_property_ids(self):
        """
        Gathers all of the property ids for each listing
        """
        if not self.table_div:
            logging.error(f'The Sheriff Sale Table Div for {self.county_name} County was not captured')
            return []

        if self.listings is None:
            self.get_all_listings()

        property_ids = [listing['property_id'] for listing in self.listings]

        return property_ids

    def get_all_listing_sheriff_ids(self):
        """
        Gathers all the sheriff id's from the table_data
        'F-18001491'
        """

        if self.listings is None:
            self.get_all_listings()

        sheriff_ids = [listing['sheriff_id'] for listing in self.listings]

        return sheriff_ids

    def get_all_listing_address(self):
        """
        Gathers all of the address data for each listing
        """
        if self.listings is None:
            self.get_all_listings()

        addresses = [listing['address'] for listing in self.listings]

        return addresses

    def get_all_listing_sale_dates(self):
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

    def get_new_listing_details_html(self, property_id):
        """
        Gathers all table html data from listings that do not exist within the database yet.
        """
        listing_details_url = f'https://salesweb.civilview.com/Sales/SaleDetails?PropertyId={property_id}'
        listing_details_html = requests_content(listing_details_url, self.session)

        return listing_details_html

    def get_listing_details_and_status_history(self, use_google_map_api: bool):
        property_ids = self.get_all_listing_property_ids()
        listing_soups = [self.get_new_listing_details_html(property_id) for property_id in property_ids]

        all_listings = []
        for listing_soup in listing_soups:
            listing = SheriffSaleListing(listing_html=listing_soup, county=self.county_name).parse(use_google_map_api)
            status_history = SheriffSaleStatusHistory(listing_html=listing_soup).parse()
            all_listings.append({'listing': listing, 'status_history': status_history})

        return all_listings
