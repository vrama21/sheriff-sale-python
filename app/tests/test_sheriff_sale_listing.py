import codecs
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from app.services.sheriff_sale import SheriffSaleListing


@pytest.fixture
def parsed_listing_html():
    listing_html_path = Path(__file__).resolve().parent / 'data' / 'listing_detail.html'

    html_file = None
    with codecs.open(listing_html_path, 'r', 'utf-8') as html_file_reader:
        html_file = html_file_reader.read()

    soup = BeautifulSoup(html_file, 'html.parser')

    return soup


def test_parse_listing_details(parsed_listing_html):
    sheriff_sale_listing = SheriffSaleListing(listing_html=parsed_listing_html, county='Atlantic')
    sheriff_sale_listing.parse_listing_details()

    assert sheriff_sale_listing.attorney == 'Fein, Such, Kahn & Shepard P.C.'
    assert sheriff_sale_listing.court_case == 'F-5811-20'
    assert (
        sheriff_sale_listing.defendant
        == 'TTK Investments LLC, A Deleware Limited Liability Company, et als; Emily K. Vu; State of New Jersey'
    )
    assert (
        sheriff_sale_listing.maps_url
        == 'https://www.google.com/maps/search/2515+English+Creek+Avenue+Egg+Harbor+Township+NJ+08234'
    )
    assert sheriff_sale_listing.plaintiff == 'Anchor Loans, LP'
    assert sheriff_sale_listing.priors == '3rd Party Tax Sale Cert No.: 19-00154 $5,424.85'
    assert sheriff_sale_listing.sale_date == '4/22/2021'
    assert sheriff_sale_listing.sheriff_id == 'F-21000099'
    assert sheriff_sale_listing.raw_address == '2515 English Creek Avenue Egg Harbor Township NJ 08234'
    assert sheriff_sale_listing.judgment == 145099.02


@pytest.mark.parametrize(
    (
        'county',
        'raw_address',
        'expected_street',
        'expected_city',
        'expected_unit',
        'expected_secondary_unit',
        'expected_zip_code',
    ),
    [
        (
            'Atlantic',
            '2515 English Creek Avenue Egg Harbor Township NJ 08234',
            '2515 English Creek Ave',
            'Egg Harbor Township',
            None,
            None,
            '08234',
        ),
        (
            'Bergen',
            '388 Pathway Manor Wyckoff NJ 07481',
            '388 Pathway Mnr',
            'Wyckoff',
            None,
            None,
            '07481',
        ),
        (
            'Hudson',
            '117 Kensington Avenue Apt. 101 A/K/A 117 - 121 Kensington Ave',
            '117 Kensington Ave',
            None,
            '101',
            None,
            None,
        )
    ],
)
def test_sanitize_address(
    county,
    raw_address,
    expected_street,
    expected_city,
    expected_unit,
    expected_secondary_unit,
    expected_zip_code,
):
    sheriff_sale_listing = SheriffSaleListing(listing_html=None, county=county)
    sheriff_sale_listing.raw_address = raw_address
    sheriff_sale_listing.sanitize_address()

    assert sheriff_sale_listing.county == county
    assert sheriff_sale_listing.street == expected_street
    assert sheriff_sale_listing.city == expected_city
    assert sheriff_sale_listing.unit == expected_unit
    assert sheriff_sale_listing.secondary_unit == expected_secondary_unit
    assert sheriff_sale_listing.zip_code == expected_zip_code
