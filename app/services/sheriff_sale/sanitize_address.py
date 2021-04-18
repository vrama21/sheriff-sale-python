import re
from .match_parser import match_parser
from .parse_google_maps import get_coordinates_from_address
from ...constants import (
    ADDRESS_REGEX_SPLIT,
    SUFFIX_ABBREVATIONS,
)
from ...utils import load_json_data


def sanitize_address(address: str, county: str) -> dict:
    """
    Sanitizes an address into separated properties of
    (street, city, county, unit, secondary_unit, zip_code)

    :param address: Address to sanitize
    :param county: County to sanitize

    :return: A sanitized address
    """
    if not address:
        return {}

    cities_by_county_mapping = load_json_data('data/cities_by_county_mapping.json')
    cities = cities_by_county_mapping[county]['cities']

    regex_street = re.compile(r'.*?(?:' + r'|'.join(ADDRESS_REGEX_SPLIT) + r')')
    regex_city = re.compile(r'(' + '|'.join(cities) + r')(?:[.,`\s]+)?(?:[\(\w\s\)]+)?(NJ|Nj)')
    regex_unit = re.compile(r'(Unit|Apt).([0-9A-Za-z-]+)')
    regex_secondary_unit = re.compile(r'(Building|Estate) #?([0-9a-zA-Z]+)')
    regex_zip_code = re.compile(r'\d{5}')

    street_match = match_parser(regex_street, address, regex_name='street')
    city_match = match_parser(regex_city, address, regex_name='city', regex_group=1)
    unit_match = match_parser(regex_unit, address, regex_name='unit', log=False)
    secondary_unit_match = match_parser(regex_secondary_unit, address, regex_name='secondary_unit', log=False)
    zip_code_match = match_parser(regex_zip_code, address, regex_name='zip_code', log=False)

    coordinates = get_coordinates_from_address(address)

    if street_match:
        for key, value in SUFFIX_ABBREVATIONS.items():
            street_match = re.sub(key, value, street_match)

    return {
        'city': city_match,
        'county': county,
        'latitude': coordinates and coordinates['lat'],
        'longitude': coordinates and coordinates['lng'],
        'street': street_match,
        'unit': unit_match,
        'unit_secondary': secondary_unit_match,
        'zip_code': zip_code_match,
    }
