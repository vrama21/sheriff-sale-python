
# URLS
nj_parcels_url = 'http://njparcels.com/property/'
nj_parcels_api_url = 'http://njparcels.com/api/v1.0/property/'
sheriff_sales_url = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=25'
trulia_url = 'https://www.trulia.com/'

# Dictionaries
replace_dict = {
    'Avenue': 'Ave',
    'Building': 'Bldg',
    'Boulevard': 'Blvd',
    'Circle': 'Cir',
    'Court': 'Ct',
    'Drive': 'Dr',
    'East': 'E',
    'Road': 'Rd',
    'Lane': 'Ln',
    'North': 'N',
    'Place': 'Pl',
    'South': 'S',
    'Square': 'Sq',
    'Street': 'St',
    'Terrace': 'Terr',
    'West': 'W'
}

city_list = [
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
    'Northfield',
    'Pleasantville',
    'Port Republic',
    'Somers Point',
    'Ventnor City',
    'Weymouth',
    'Williamstown'
]

city_zip_dict = {
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

street_suffix = [
    'Ave',
    'Blvd',
    'Cir',
    'Croft',
    'Club',
    'Ct',
    'Dr',
    'Rd',
    'Ln',
    'Pike',
    'Pl',
    'Run',
    'Sq',
    'St',
    'Terr',
    'Way'
]
remove_list = ['NJ',
               '08232',
               '08234',
               '08201',
               '08205',
               '08232']