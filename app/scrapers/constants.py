import itertools
from pathlib import Path
from utils import load_json_data

NJ_PARCELS_URL = "http://njparcels.com/property/"
NJ_PARCELS_API = "http://njparcels.com/api/v1.0/property/"
SHERIFF_SALES_BASE_URL = "https://salesweb.civilview.com"
SHERIFF_SALES_URL = "https://salesweb.civilview.com/Sales/SalesSearch?countyId="

SHERIFF_SALE_JSON_DATA = load_json_data("SheriffSaleCountyID.json")
NJPARCELS_JSON_DATA = load_json_data("NJParcels_CityNums.json")
TEST_JSON_DATA = load_json_data("test.json")
test = load_json_data("test.json")
COUNTY_LIST = sorted(list(NJPARCELS_JSON_DATA.keys()))
CITY_LIST = sorted(itertools.chain.from_iterable([NJPARCELS_JSON_DATA[x].keys() for x in COUNTY_LIST]))

SUFFIX_ABBREVATIONS = {
    "Avenue": "Ave",
    "Building": "Bldg",
    "Boulevard": "Blvd",
    "Circle": "Cir",
    "Court": "Ct",
    "Drive": "Dr",
    "East": "E",
    "Lane": "Ln",
    "North": "N",
    "Place": "Pl",
    "Road": "Rd",
    "South": "S",
    "Square": "Sq",
    "Street": "St",
    "Terrace": "Terr",
    "West": "W",
}

ADDRESS_REGEX_SPLIT = [
    "Argyle",  # (Edge Case)
    "Avenue",
    "Bay",
    "Boardwalk",
    "Boulevard",
    "Circle",
    "Condo",  # (Edge Case)
    "Cove",
    "Croft",
    "Court",
    "Drive",
    "Lane",
    "Highway",
    "Hollow",  # (Edge Case)
    "Mews",  # (Edge Case)
    "Pike",
    "Place",
    "Road",
    "Route [0-9]+",
    "Run",
    "Square",
    "Street",
    "Terrace",
    "Trail",
    "Village",
    "Way",
]

CITY_LIST_SANITIZED = {
    "Atlanic City": "Atlantic City",
    "Buena Boro": "Buena",
    "Buena Borough": "Buena",
    "Margate City": "Margate",
    "Pomona": "Galloway Township",
}

