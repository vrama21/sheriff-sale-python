import bs4
import logging
import re
from decimal import Decimal

from .sanitize_address import sanitize_address

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


def parse_listing_details(listing_html: bs4.element.Tag, county: str) -> dict:
    """
    Parses the details table of a listings detail page

    :param listing_html: A beautiful soup object to parse through
    :param county: The county that is being parsed

    :return: A dictionary of parsed data points
    """
    listing_table = listing_html.find('table', class_='table table-striped')
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
            return

        if key == 'address':
            address_br = td[1].find('br')
            value = f'{address_br.previous_element} {address_br.next_element}'.strip().title()
        elif key == 'attorney_phone' and (td[1] is not None or not ''):
            clean_phone_number = re.sub('[^0-9]', '', value)
            formatted_phone_number = f'{clean_phone_number[0:3]}-{clean_phone_number[3:6]}-{clean_phone_number[6:10]}'
            value = formatted_phone_number
        elif key == 'judgment' or key == 'upset_amount':
            clean_value = Decimal(re.sub(r'[^\d.]', ''), value)
            value = clean_value

        elif value == '':
            value = None

        listing_details[key] = value

    listing_details['maps_url'] = maps_url and maps_url['href']

    address_sanitized = sanitize_address(address=listing_details['address'], county=county)

    listing_details = {**listing_details, **address_sanitized}

    return listing_details
