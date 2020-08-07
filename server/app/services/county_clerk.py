import requests
from flask_sqlalchemy import SQLAlchemy

from .. import db, models


def county_clerk_search(name, headers=False, doctypes=None):
    county_clerk_search_url = 'http://24.246.110.8/or_web1/api/search'

    if doctypes:
        doctypes = doctypes

    body = {
        'DocTypes': doctypes,
        'Party': name,
        'MaxRows': 0,
        'RowsPerPage': 0,
        'StartRow': 0
    }

    response = requests.post(county_clerk_search_url, data=body)
    json_response = response.json()

    if not headers:
        del json_response[0]['_headers']
        del json_response[0]['_end_row']
        del json_response[0]['_max_rows']
        del json_response[0]['_start_row']
        del json_response[0]['_total_rows']

    return json_response


def county_clerk_document(doc_id):
    county_clerk_document_url = 'http://24.246.110.8/or_web1/api/document'

    body = {
        'ID': doc_id,
    }

    response = requests.post(county_clerk_document_url, data=body)
    json_response = response.json()

    return json_response
