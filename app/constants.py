from pathlib import Path
from pprint import PrettyPrinter

from .utils import load_json_data

ROOT_DIR = Path(__file__).parent.parent
BUILD_DIR = ROOT_DIR / 'build'
LOG_DIR = ROOT_DIR / 'logs'
STATIC_DIR = ROOT_DIR / 'build' / 'static'

NJ_DATA = load_json_data('data/NJ_Data.json')
COUNTY_LIST = sorted(list(NJ_DATA.keys()))
COUNTY_MAP = [
    NJ_DATA[county]['sheriffSaleId']
    for county in COUNTY_LIST
    if NJ_DATA[county]['sheriffSaleId'] != ''
]

PRETTIFY = PrettyPrinter(2)

SUFFIX_ABBREVATIONS = {
    'Avenue': 'Ave',
    'Building': 'Bldg',
    'Boulevard': 'Blvd',
    'Circle': 'Cir',
    'Court': 'Ct',
    'Drive': 'Dr',
    'East': 'E',
    'Lane': 'Ln',
    'North': 'N',
    'Place': 'Pl',
    'Road': 'Rd',
    'South': 'S',
    'Square': 'Sq',
    'Street': 'St',
    'Terrace': 'Terr',
    'West': 'W',
}

ADDRESS_REGEX_SPLIT = [
    'Argyle',  # (Edge Case)
    'Ave',
    'Avenue',
    'Bay',
    'Boardwalk',
    'Boulevard',
    'Broadway',
    'Circle',
    'Condo',  # (Edge Case)
    'Cove',
    'Croft',
    'Court',
    'Drive',
    'Lane',
    'Highway',
    'Hollow',  # (Edge Case)
    'Mews',  # (Edge Case)
    'Pkwy',
    'Parkway',
    'Pike',
    'Place',
    'Road',
    'Route [0-9]+',
    'Run',
    'Square',
    'Street',
    'Terrace',
    'Trail',
    'Village',
    'Way',
]