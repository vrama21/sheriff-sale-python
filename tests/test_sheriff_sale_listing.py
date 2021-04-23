import codecs
import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

# from app.constants import
from app.services.sheriff_sale import SheriffSaleListing


def test_parse_listing_details(client, auth):
    listing_html_path = Path(__file__).resolve().parent / 'listing_detail.html'

    html_file = None
    with codecs.open(listing_html_path, 'r', 'utf-8') as html_file_reader:
        html_file = html_file_reader.read()

    soup = BeautifulSoup(html_file, 'html.parser')
    sheriff_sale_listing = SheriffSaleListing(listing_html=soup, county='Atlantic')
    sheriff_sale_listing.parse_listing_details()

    print(sheriff_sale_listing.raw_address)
    assert sheriff_sale_listing.judgment == '$145,099.02'

    # print(html_file)
    # county = 'Atlantic'
