import requests
from flask_sqlalchemy import SQLAlchemy

from .. import db, models

doc_types_liens = [
    'CNLA', 'CNL', 'CLC', 'CLCD', 'DEMM', 'CNLD', 'AIRD', 'DNA', 'FTL', 'HL', 'ILV', 'ILD', 'MECH LN', 'MEDL', 'MULC',
    'NOL', 'VL', 'FTLW'
]


def county_clerk_search(name, headers=False, doctypes=None):
    county_clerk_search_url = 'http://24.246.110.8/or_web1/api/search'

    if doctypes:
        doctypes = doctypes

    body = {'DocTypes': doctypes, 'Party': name, 'MaxRows': 0, 'RowsPerPage': 0, 'StartRow': 0}

    response = requests.post(county_clerk_search_url, data=body)
    json_response = response.json()

    if not headers:
        keys_to_remove = ['_headers', '_end_row', '_max_rows', '_start_row', '_total_rows']
        for key in keys_to_remove:
            del json_response[0][key]

    return json_response


def county_clerk_document(doc_id):
    county_clerk_document_url = 'http://24.246.110.8/or_web1/api/document'

    body = {
        'ID': doc_id,
    }

    response = requests.post(county_clerk_document_url, data=body)
    json_response = response.json()

    return json_response


def doc_type_mapper():
    url = 'http://24.246.110.8/or_web1/api/document/doctypes'

    response = requests.get(url)
    json_response = response.json()

    doc_type_mapping = {}
    for doc_type in json_response:
        doc_type_mapping[doc_type['value']] = doc_type['name']

    return doc_type_mapping
