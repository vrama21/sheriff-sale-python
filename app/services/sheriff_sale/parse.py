import logging
from .sanitize_address import sanitize_address

logging = logging.getLogger(__name__)

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


def parse(listing_html: str, county: str):
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

        try:
            key = LISTING_KV_MAP[label]
            value = None
            if key == 'address':
                address_br = td[1].find('br')
                value = f'{address_br.previous_element} {address_br.next_element}'.strip().title()
            else:
                value = td[1].text.strip().title()
                if value == '':
                    value = None

            listing_details[key] = value
        except KeyError:
            logging.error(f'Missing Key: "{label}" listing_kv_mapping')

    listing_details['maps_url'] = maps_url and maps_url['href']

    address_sanitized = sanitize_address(
        address=listing_details['address'], county=county
    )

    listing_details = {**listing_details, **address_sanitized}

    status_history_html = listing_html.find('table', id='longTable')

    status_history = []
    if status_history_html is not None:
        for tr in status_history_html.find_all('tr')[1:]:
            td = tr.find_all('td')
            listing_status = {
                'status': td[0].text.strip(),
                'date': td[1].text.strip(),
            }
            status_history.append(listing_status)

    return {'listing_details': listing_details, 'status_history': status_history}
