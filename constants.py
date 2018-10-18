
NJ_PARCELS_URL = 'http://njparcels.com/property/'
NJ_PARCELS_API = 'http://njparcels.com/api/v1.0/property/'
SHERIFF_SALES_URL = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=25'
SHERIFF_SALES_BASE_URL = 'https://salesweb.civilview.com'

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
    'West': 'W'
}

ADDRESS_REGEX_SPLIT = [
    'Avenue',
    'Boardwalk',
    'Boulevard',
    'Circle',
    'Cove',
    'Croft',
    'Court',
    'Drive',
    'Lane',
    'Pike',
    'Place',
    'Road',
    'Route',
    'Square',
    'Street',
    'Terrace',
    'Village',
    'Way'
]

CITY_LIST = [
    'Absecon',
    'Atlantic City',
    'Brigantine',
    'Buena',
    'Buena Vista Township',
    'Corbin City',
    'Egg Harbor City',
    'Egg Harbor Township',
    'Estell Manor',
    'Galloway Township',
    'Hamilton Township',
    'Hammonton',
    'Linwood',
    'Longport',
    'Margate',
    'Mays Landing',
    'Mullica Township',
    'Newtonville',
    'Northfield',
    'Pleasantville',
    'Port Republic',
    'Somers Point',
    'Ventnor City',
    'Weymouth',
    'Williamstown'
]

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
    "Ventnor City": "08406"
}
