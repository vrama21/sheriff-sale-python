from pathlib import Path
from pprint import PrettyPrinter
import re

from .utils import load_json_data

ROOT_DIR = Path(__file__).parent.parent
APP_DIR = Path(__file__).parent

BUILD_DIR = ROOT_DIR / 'build'
MIGRATIONS_DIR = ROOT_DIR / 'migrations'
LOG_DIR = ROOT_DIR / 'logs'
SCRIPTS_DIR = APP_DIR / 'scripts'
STATIC_DIR = ROOT_DIR / 'build' / 'static'

NJ_DATA = load_json_data('data/NJ_Data.json')
CITIES_BY_COUNTY = load_json_data('data/cities_by_county_mapping.json')
COUNTY_LIST = sorted(list(NJ_DATA.keys()))
COUNTY_MAP = [NJ_DATA[county]['sheriffSaleId'] for county in COUNTY_LIST if NJ_DATA[county]['sheriffSaleId'] != '']

PRETTIFY = PrettyPrinter(2)

NJ_SHERIFF_SALE_COUNTIES = [
    'Atlantic',
    'Bergen',
    'Burlington',
    'Camden',
    'Cumberland',
    'Essex',
    'Hudson',
    'Hunterdon',
    'Monmouth',
    'Morris',
    'Passaic',
    'Salem',
    'Union',
]

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
