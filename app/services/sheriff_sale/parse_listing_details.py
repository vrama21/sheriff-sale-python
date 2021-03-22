import logging
import re
from .sanitize_address import sanitize_address

logging = logging.getLogger(__name__)
print(logging)

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


def parse_listing_details(listing_html: str, county: str):
    """
    Parameters:
        listing_html (soup): A beautiful soup object to parse through
        county (str): The county that is being parsed

    Returns:
        A dictionary of parsed data points
    """
    listing_table = listing_html.find('table', class_='table table-striped')
    maps_url = listing_table.find('a', href=True)

    listing_details = {}
    for tr in listing_table.find_all('tr'):
        td = tr.find_all('td')
        label = td[0].text.replace('&colon', '')

        key = LISTING_KV_MAP.get(label)
        value = None

        if not key:
            logging.error(f'Missing Key: "{label}" listing_kv_mapping')

        if key == 'address':
            address_br = td[1].find('br')
            value = f'{address_br.previous_element} {address_br.next_element}'.strip().title()
        elif key == 'attorney_phone' and td[1] is not None or not '':
            phone_regex = re.compile(r'(?:\d|\d{3,4})+')
            matches = re.findall(phone_regex, td[1].text.strip())
            value = '-'.join(matches[0:3])
        else:
            value = td[1].text.strip().title()
            if value == '':
                value = None

        listing_details[key] = value

    listing_details['maps_url'] = maps_url and maps_url['href']

    address_sanitized = sanitize_address(
        address=listing_details['address'], county=county
    )

    listing_details = {**listing_details, **address_sanitized}

    return listing_details
