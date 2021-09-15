from __future__ import annotations
from dataclasses import dataclass

import logging
from typing import Union

import regex
from bs4 import BeautifulSoup

import app.services.google_maps as google_maps_service
from app.constants import ADDRESS_REGEX_SPLIT, SUFFIX_ABBREVATIONS
from app.utils import load_json_data, match_parser

LISTING_KV_MAP = {
    'Address': 'raw_address',
    'Approx Judgment': 'judgment',
    'Approx Upset': 'upset_amount',
    'Attorney': 'attorney',
    'Attorney Phone': 'attorney_phone',
    'Court Case': 'court_case',
    'Deed': 'deed',
    'Deed Address': 'deed_address',
    'Defendant': 'defendant',
    'Description': 'description',
    'Judgment Amount': 'judgment',
    'Parcel': 'parcel',
    'Plaintiff': 'plaintiff',
    'Priors': 'priors',
    'Sales Date': 'sale_date',
    'Sheriff': 'sheriff_id',
    'Upset Amount': 'upset_amount',
}


@dataclass
class SheriffSaleListing:
    listing_html: Union[BeautifulSoup, None] = None

    address: Union[str, None] = None
    attorney: Union[str, None] = None
    attorney_phone: Union[str, None] = None
    city: Union[str, None] = None
    county: Union[str, None] = None
    court_case: Union[str, None] = None
    deed: Union[str, None] = None
    deed_address: Union[str, None] = None
    defendant: Union[str, None] = None
    description: Union[str, None] = None
    judgment: Union[float, None] = None
    latitude: Union[str, None] = None
    longitude: Union[str, None] = None
    maps_url: Union[str, None] = None
    parcel: Union[str, None] = None
    plaintiff: Union[str, None] = None
    priors: Union[str, None] = None
    property_id: int = None
    raw_address: Union[str, None] = None
    sale_date: Union[str, None] = None
    secondary_unit: Union[str, None] = None
    sheriff_id: Union[str, None] = None
    state: Union[str, None] = 'NJ'
    street: Union[str, None] = None
    unit: Union[str, None] = None
    unit_secondary: Union[str, None] = None
    upset_amount: Union[float, None] = None
    zip_code: Union[str, None] = None

    # def __init__(self, county: str, listing_html: Union[BeautifulSoup, None], property_id: int):
    #     self.listing_html = listing_html

    #     self.address: Union[str, None] = None
    #     self.attorney: Union[str, None] = None
    #     self.attorney_phone: Union[str, None] = None
    #     self.city: Union[str, None] = None
    #     self.county: Union[str, None] = county
    #     self.court_case: Union[str, None] = None
    #     self.deed: Union[str, None] = None
    #     self.deed_address: Union[str, None] = None
    #     self.defendant: Union[str, None] = None
    #     self.description: Union[str, None] = None
    #     self.judgment: Union[float, None] = None
    #     self.latitude: Union[str, None] = None
    #     self.longitude: Union[str, None] = None
    #     self.maps_url: Union[str, None] = None
    #     self.parcel: Union[str, None] = None
    #     self.plaintiff: Union[str, None] = None
    #     self.priors: Union[str, None] = None
    #     self.property_id: int = property_id
    #     self.raw_address: Union[str, None] = None
    #     self.sale_date: Union[str, None] = None
    #     self.secondary_unit: Union[str, None] = None
    #     self.sheriff_id: Union[str, None] = None
    #     self.state: Union[str, None] = 'NJ'
    #     self.street: Union[str, None] = None
    #     self.unit: Union[str, None] = None
    #     self.unit_secondary: Union[str, None] = None
    #     self.upset_amount: Union[float, None] = None
    #     self.zip_code: Union[str, None] = None

    # def __dict__(self) -> dict:
    #     return {
    #         'address': self.address,
    #         'attorney': self.attorney,
    #         'attorney_phone': self.attorney_phone,
    #         'city': self.city,
    #         'county': self.county,
    #         'court_case': self.court_case,
    #         'deed': self.deed,
    #         'deed_address': self.deed_address,
    #         'defendant': self.defendant,
    #         'description': self.description,
    #         'judgment': self.judgment,
    #         'latitude': self.latitude,
    #         'longitude': self.longitude,
    #         'maps_url': self.maps_url,
    #         'parcel': self.parcel,
    #         'plaintiff': self.plaintiff,
    #         'priors': self.priors,
    #         'property_id': self.property_id,
    #         'raw_address': self.raw_address,
    #         'sale_date': self.sale_date,
    #         'secondary_unit': self.secondary_unit,
    #         'sheriff_id': self.sheriff_id,
    #         'state': self.state,
    #         'street': self.street,
    #         'unit': self.unit,
    #         'unit_secondary': self.unit_secondary,
    #         'upset_amount': self.upset_amount,
    #         'zip_code': self.zip_code,
    #     }

    # def __repr__(self) -> str:
    #     return str(self.__dict__())

    def parse_listing_details(self) -> None:
        """
        Parses the details table of a listings detail page
        """
        listing_table = self.listing_html.find('table', class_='table table-striped')
        listing_table_rows = listing_table.find_all('tr')
        maps_url = listing_table.find('a', href=True)

        listing_details = {}
        for rows in listing_table_rows:
            td = rows.find_all('td')

            label_regex = regex.compile(r'\s?[?=\#\&\.\*\:]+(colon)?')
            listing_detail_label: str = regex.sub(label_regex, '', td[0].text)
            listing_detail_value: Union[str, float] = regex.sub(r'\s\s+', ' ', td[1].text.strip())

            key = LISTING_KV_MAP.get(listing_detail_label)

            if not key:
                logging.error(f'Missing Key: "{listing_detail_label}" listing_kv_mapping')
                return

            if listing_detail_value:
                if key == 'raw_address':
                    address_br = td[1].find('br')
                    raw_address = f'{address_br.previous_element} {address_br.next_element}'
                    listing_detail_value = raw_address
                elif key == 'attorney_phone':
                    clean_phone_number = regex.sub('[^0-9]', '', listing_detail_value)
                    listing_detail_value = (
                        f'{clean_phone_number[0:3]}-{clean_phone_number[3:6]}-{clean_phone_number[6:10]}'
                    )
                elif key == 'judgment' or key == 'upset_amount':
                    listing_detail_value = float(regex.sub(r'[^\d.]', '', listing_detail_value))

            if listing_detail_value == '':
                listing_detail_value = None

            if isinstance(listing_detail_value, str):
                listing_detail_value = listing_detail_value.strip()

            listing_details[key] = listing_detail_value

        listing_details['maps_url'] = maps_url and maps_url['href']

        for key, listing_detail_value in listing_details.items():
            setattr(self, key, listing_detail_value)

    def sanitize_address(self) -> None:
        """
        Sanitizes an address into separated properties of
        (street, city, county, unit, secondary_unit, zip_code)
        """
        if not self.raw_address:
            return

        cities_by_county_mapping = load_json_data('data/cities_by_county_mapping.json')
        cities = [city.upper() for city in cities_by_county_mapping[self.county]['cities']]

        street_split = r'|'.join(ADDRESS_REGEX_SPLIT)
        city_split = r'|'.join(cities)

        regex_street = regex.compile(fr'[\w\s]+(?<={street_split})')
        regex_city = regex.compile(fr'({city_split})(?:[.,`\s]+)?(?:[\(\w\s\)]+)?(NJ)')
        regex_unit = regex.compile(r'(UNIT|APT)[\.\s#]+?([0-9A-Za-z-]+)')
        regex_secondary_unit = regex.compile(r'(BUILDING|ESTATE)[\s#]+?([0-9a-zA-Z]+)')
        regex_zip_code = regex.compile(r'\d{5}')

        street_match = match_parser(regex_street, target=self.raw_address, regex_name='street')
        city_match = match_parser(regex_city, target=self.raw_address, regex_name='city', regex_group=1)
        unit_match = match_parser(regex_unit, target=self.raw_address, regex_group=2, regex_name='unit', log=False)
        secondary_unit_match = match_parser(
            regex_secondary_unit, target=self.raw_address, regex_name='secondary_unit', log=False
        )
        zip_code_match = match_parser(regex_zip_code, target=self.raw_address, regex_name='zip_code', log=False)

        if street_match:
            for key, value in SUFFIX_ABBREVATIONS.items():
                street_match = regex.sub(key, value, street_match)

        self.address = (
            street_match and city_match and zip_code_match and f'{street_match}, {city_match} {zip_code_match}'
        )
        self.street = street_match
        self.city = city_match
        self.unit = unit_match
        self.unit_secondary = secondary_unit_match
        self.zip_code = zip_code_match

    def get_coordinates(self) -> None:
        """
        Gets the coordinates of a given address using google maps API
        """
        formatted_address = f'{self.street}, {self.city}, {self.state}'

        coordinates = google_maps_service.get_coordinates_from_address(formatted_address)

        if coordinates:
            self.latitude = coordinates['lat']
            self.longitude = coordinates['lng']

    def parse(self, use_google_maps_api: bool = True) -> SheriffSaleListing:
        """
        Runs all the parsing functions

        :param use_google_maps_api: Whether to get coordinates from google maps API or not

        :returns A clean Listing
        """
        self.parse_listing_details()
        self.sanitize_address()

        if use_google_maps_api:
            self.get_coordinates()

        return self
