import logging

import regex

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
        self.raw_address: str = None
        self.sale_date: str = None
        self.secondary_unit: str = None
        self.sheriff_id: str = None
        self.state: str = 'NJ'
        self.street: str = None
        self.unit: str = None
        self.unit_secondary: str = None
        self.upset_amount: float = None
        self.zip_code: str = None

    def __dict__(self):
        return {
            'address': None,
            'attorney': None,
            'attorney_phone': None,
            'city': None,
            'county': self.county,
            'court_case': None,
            'deed': None,
            'deed_address': None,
            'defendant': None,
            'description': None,
            'judgment': None,
            'latitude': None,
            'longitude': None,
            'maps_url': None,
            'parcel': None,
            'plaintiff': None,
            'priors': None,
            'raw_address': None,
            'sale_date': None,
            'secondary_unit': None,
            'sheriff_id': None,
            'state': self.state,
            'street': None,
            'unit': None,
            'unit_secondary': None,
            'upset_amount': None,
            'zip_code': None,
        }

    def __repr__(self) -> str:
        self.__dict__()

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

            listing_detail_label: str = td[0].text
            listing_detail_value: str = td[1].text

            label_regex = regex.compile(r'\s?[?=\#\&\.\*\:]+(colon)?')
            label: str = regex.sub(label_regex, '', listing_detail_label)

            value = listing_detail_value.strip()

            key = LISTING_KV_MAP.get(label)

            if not key:
                logging.error(f'Missing Key: "{label}" listing_kv_mapping')
                return {}

            if value:
                if key == 'raw_address':
                    address_br = td[1].find('br')
                    raw_address = f'{address_br.previous_element} {address_br.next_element}'.strip()
                    value = raw_address
                elif key == 'attorney_phone':
                    clean_phone_number = regex.sub('[^0-9]', '', value)
                    formatted_phone_number = (
                        f'{clean_phone_number[0:3]}-{clean_phone_number[3:6]}-{clean_phone_number[6:10]}'
                    )
                    value = formatted_phone_number
                elif key == 'judgment' or key == 'upset_amount':
                    clean_value = float(regex.sub(r'[^\d.]', '', value))
                    value = clean_value

            if value == '':
                value = None

            listing_details[key] = value

        listing_details['maps_url'] = maps_url and maps_url['href']

        for key, value in listing_details.items():
            setattr(self, key, value)

    def sanitize_address(self):
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

    def get_coordinates(self):
        """
        Gets the coordinates of a given address using google maps API
        """
        formatted_address = f'{self.street}, {self.city}, {self.state}'

        coordinates = google_maps_service.get_coordinates_from_address(formatted_address)

        if coordinates:
            self.latitude = coordinates['lat']
            self.longitude = coordinates['lng']

    def parse(self, use_google_maps_api: bool = True):
        """
        Runs all the parsing functions

        :param use_google_maps_api: Whether to get coordinates from google maps API or not

        :returns A clean Listing
        """
        self.parse_listing_details()
        self.sanitize_address()
        use_google_maps_api and self.get_coordinates()

        return self
