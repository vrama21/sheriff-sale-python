import re
from . import match_parser
from ...constants import (
    ADDRESS_REGEX_SPLIT,
    CITY_LIST,
    SUFFIX_ABBREVATIONS,
)


def sanitize_address(address: str, county: str) -> dict:
    """
    Sanitizes an address into separated properties of
    (street, city, county, unit, secondary_unit, zip_code)

    :param address: Address to sanitize
    :param county: County to sanitize

    :return: A sanitized address
    """
    regex_street = re.compile(r'.*?(?:' + r'|'.join(ADDRESS_REGEX_SPLIT) + r')\s')
    regex_city = re.compile(r'(' + '|'.join(CITY_LIST) + ') (NJ|Nj)')
    regex_unit = re.compile(r'(Unit|Apt).([0-9A-Za-z-]+)')
    regex_secondary_unit = re.compile(r'(Building|Estate) #?([0-9a-zA-Z]+)')
    regex_zip_code = re.compile(r'\d{5}')

    street_match = match_parser(regex_street, address, regex_name='street')
    city_match = match_parser(regex_city, address, regex_name='city', regex_group=1)
    unit_match = match_parser(regex_unit, address, regex_name='unit', log=False)
    secondary_unit_match = match_parser(regex_secondary_unit, address, regex_name='secondary_unit', log=False)
    zip_code_match = match_parser(regex_zip_code, address, regex_name='zip_code', log=False)

    if street_match:
        for key, value in SUFFIX_ABBREVATIONS.items():
            street_match = re.sub(key, value, street_match)

    return {
        'city': city_match,
        'county': county,
        'street': street_match,
        'unit': unit_match,
        'unit_secondary': secondary_unit_match,
        'zip_code': zip_code_match,
    }
