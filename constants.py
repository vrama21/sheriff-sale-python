from pathlib import Path

NJ_PARCELS_URL = "http://njparcels.com/property/"
NJ_PARCELS_API = "http://njparcels.com/api/v1.0/property/"
SHERIFF_SALES_URL = "https://salesweb.civilview.com/Sales/SalesSearch?countyId=25"
SHERIFF_SALES_BASE_URL = "https://salesweb.civilview.com"

BASE_DIR = Path(__file__).resolve().parent
FLASK_APP_DIR = BASE_DIR.joinpath("flask_app")

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

CITY_LIST = [
    "Absecon",
    "Atlantic City",
    "Brigantine",
    "Buena",
    "Buena Boro",
    "Buena Borough",
    "Buena Vista",
    "Buena Vista Township",
    "Corbin City",
    "Dorothy",
    "Egg Harbor City",
    "Egg Harbor Township",
    "Elwood",
    "Estell Manor",
    "Folsom",
    "Galloway Township",
    "Hamilton Township",
    "Hammonton",
    "Landisville",
    "Linwood",
    "Longport",
    "Margate City",
    "Mays Landing",
    "Minotola",
    "Mullica Township",
    "Newtonville",
    "Northfield",
    "Pleasantville",
    "Pomona",
    "Port Republic",
    "Richland",
    "Somers Point",
    "Smithville",
    "Ventnor City",
    "Vineland",
    "Weymouth",
    "Weymouth Township",
    "Williamstown",
]

CITY_LIST_SANITIZED = {
    "Atlanic City": "Atlantic City",
    "Buena Boro": "Buena",
    "Buena Borough": "Buena",
    "Margate City": "Margate",
    "Pomona": "Galloway Township",
}

CITY_ZIP_DICT = {
    "Absecon": "08201",
    "Atlantic City": "08401",
    "Brigantine": "08203",
    "Buena": "[08310, 08317, 08326]",
    "Corbin City": "08270",
    "Egg Harbor City": "08215",
    "Egg Harbor Township": "08234",
    "Estell Manor": "08319",
    "Galloway Township": "08205",
    "Hammonton": "08037",
    "Linwood": "08221",
    "Longport": "08403",
    "Margate City": "08402",
    "Mays Landing": "08330",
    "Mullica Township": "08217",
    "Northfield": "08225",
    "Pleasantville": "08232",
    "Port Republic": "08241",
    "Somers Point": "08244",
    "Ventnor City": "08406",
}

COUNTIES = [
    "Atlantic",
    "Bergen",
    "Burlington",
    "Camden",
    "Cumberland",
    "Essex",
    "Gloucester",
    "Hudson",
    "Monmouth",
    "Morris",
    "Passaic",
    "Salem",
    "Union",
]
