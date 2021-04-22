import logging
import re
from datetime import datetime

from bs4.element import Tag

import app.services.google_maps as google_maps_service
from app.constants import ADDRESS_REGEX_SPLIT, SUFFIX_ABBREVATIONS
from app.utils import load_json_data, match_parser

LISTING_KV_MAP = {
    'Address': 'address',
    'Approx Judgment': 'judgment',
    'Approx. Judgment': 'judgment',
    'Approx. Judgment*': 'judgment',
    'Approx. Upset*': 'upset_amount',
    'Attorney': 'attorney',
    'Attorney Phone': 'attorney_phone',
    'Court Case #': 'court_case',
    'Deed': 'deed',
    'Deed Address': 'deed_address',
    'Defendant': 'defendant',
    'Description': 'description',
    'Judgment Amount*': 'judgment',
    'Parcel #': 'parcel',
    'Plaintiff': 'plaintiff',
    'Priors': 'priors',
    'Sales Date': 'sale_date',
    'Sheriff #': 'sheriff_id',
    'Upset Amount': 'upset_amount',
}


class SheriffSaleListing:
    def __init__(self, listing_html, county):
        self.listing_html = listing_html

        self.address: str = None
        self.attorney: str = None
        self.attorney_phone: str = None
        self.city: str = None
        self.county: str = county
        self.court_case: str = None
        self.deed: str = None
        self.deed_address: str = None
        self.defendant: str = None
        self.description: str = None
        self.judgment: float = None
        self.latitude: str = None
        self.longitude: str = None
        self.maps_url: str = None
        self.parcel: str = None
        self.plaintiff: str = None
        self.priors: str = None
        self.sale_date: str = None
        self.secondary_unit: str = None
        self.state: str = 'NJ'
        self.status_history: str = None
        self.street: str = None
        self.unit: str = None
        self.unit_secondary: str = None
        self.upset_amount: float = None
        self.zip_code: str = None

    def parse_listing_details(self):
        """
        Parses the details table of a listings detail page
        """
        listing_table = self.listing_html.find('table', class_='table table-striped')
        listing_table_rows = listing_table.find_all('tr')
        maps_url = listing_table.find('a', href=True)

        listing_details = {}
        for rows in listing_table_rows:
            td = rows.find_all('td')
            label = td[0].text.replace('&colon', '')
            value = td[1].text.strip().title()

            key = LISTING_KV_MAP.get(label)

            if not key:
                logging.error(f'Missing Key: "{label}" listing_kv_mapping')
                return {}

            if key == 'address':
                address_br = td[1].find('br')
                address = f'{address_br.previous_element} {address_br.next_element}'.strip()
                value = address
            elif key == 'attorney_phone':
                if value:
                    clean_phone_number = re.sub('[^0-9]', '', value)
                    formatted_phone_number = (
                        f'{clean_phone_number[0:3]}-{clean_phone_number[3:6]}-{clean_phone_number[6:10]}'
                    )
                    value = formatted_phone_number
            elif key == 'judgment' or key == 'upset_amount':
                if value:
                    clean_value = float(re.sub(r'[^\d.]', '', value))
                    value = clean_value

            if value == '':
                value = None

            listing_details[key] = value

        listing_details['maps_url'] = maps_url and maps_url['href']

        for key, value in listing_details.items():
            setattr(self, key, value)

    def parse_status_history(self):
        """
        Parses the status history table of a listings detail page
        """
        status_history_html = self.listing_html.find('table', id='longTable')

        status_history = []
        if status_history_html is not None:
            for tr in status_history_html.find_all('tr')[1:]:
                td = tr.find_all('td')
                listing_status = {
                    'status': td[0].text.strip(),
                    'date': td[1].text.strip(),
                }
                status_history.append(listing_status)

        self.status_history = status_history

    def sanitize_address(self):
        """
        Sanitizes an address into separated properties of
        (street, city, county, unit, secondary_unit, zip_code)
        """
        if not self.address:
            return

        cities_by_county_mapping = load_json_data('data/cities_by_county_mapping.json')
        cities = cities_by_county_mapping[self.county]['cities']

        regex_street = re.compile(r'.*?(?:' + r'|'.join(ADDRESS_REGEX_SPLIT) + r')')
        regex_city = re.compile(r'(' + '|'.join(cities) + r')(?:[.,`\s]+)?(?:[\(\w\s\)]+)?(NJ|Nj)')
        regex_unit = re.compile(r'(Unit|Apt).([0-9A-Za-z-]+)')
        regex_secondary_unit = re.compile(r'(Building|Estate) #?([0-9a-zA-Z]+)')
        regex_zip_code = re.compile(r'\d{5}')

        street_match = match_parser(regex_street, target=self.address, regex_name='street')
        city_match = match_parser(regex_city, target=self.address, regex_name='city', regex_group=1)
        unit_match = match_parser(regex_unit, target=self.address, regex_name='unit', log=False)
        secondary_unit_match = match_parser(
            regex_secondary_unit, target=self.address, regex_name='secondary_unit', log=False
        )
        zip_code_match = match_parser(regex_zip_code, target=self.address, regex_name='zip_code', log=False)

        if street_match:
            for key, value in SUFFIX_ABBREVATIONS.items():
                street_match = re.sub(key, value, street_match)

        self.city = city_match
        self.street = street_match
        self.unit = unit_match
        self.unit_secondary = secondary_unit_match
        self.zip_code = zip_code_match

    def get_coordinates(self):
        """
        Gets the coordinates of a given address using google maps API
        """
        formatted_address = f'{self.street}, {self.city}, {self.state}'

        coordinates = google_maps_service.get_coordinates_from_address(formatted_address)

        if coordinates:
            self.latitude = coordinates['lat']
            self.longitude = coordinates['lng']

    def parse(self, get_coordinates: bool = True):
        """
        Runs all the parsing functions

        :param get_coordinates: Whether to get coordinates from google maps API or not

        :returns A clean Listing
        """
        self.parse_listing_details()
        self.parse_status_history()
        get_coordinates and self.get_coordinates()
        self.sanitize_address()

        return {
            'address': self.address,
            'attorney': self.attorney,
            'attorney_phone': self.attorney_phone,
            'city': self.city,
            'county': self.county,
            'court_case': self.court_case,
            'deed': self.deed,
            'deed_address': self.deed_address,
            'defendant': self.defendant,
            'description': self.description,
            'judgment': self.judgment,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'maps_url': self.maps_url,
            'parcel': self.parcel,
            'plaintiff': self.plaintiff,
            'priors': self.priors,
            'sale_date': self.sale_date,
            'secondary_unit': self.secondary_unit,
            'state': self.state,
            'status_history': self.status_history,
            'street': self.street,
            'unit': self.unit,
            'unit_secondary': self.unit_secondary,
            'upset_amount': self.upset_amount,
            'zip_code': self.zip_code,
        }
