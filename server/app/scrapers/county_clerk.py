import requests
from ..models import CountyClerk

def county_clerk_search(name, headers=False, doctypes=None):
    county_clerk_search_url = 'http://24.246.110.8/or_web1/api/search'

    if doctypes:
        doctypes = doctypes

    body = {
        "DocTypes": doctypes,
        "Party": name,
        "MaxRows": 0,
        "RowsPerPage": 0,
        "StartRow": 0
    }

    response = requests.post(county_clerk_search_url, data=body)
    json_response = response.json()

    if not headers:
        del json_response[0]['_headers']

    return json_response


def county_clerk_document(doc_id):
    county_clerk_document_url = 'http://24.246.110.8/or_web1/api/document'

    body = {
        "ID": doc_id,
        # "convert": True,
        # "page": 1
    }

    response = requests.post(county_clerk_document_url, data=body)
    json_response = response.json()

    return json_response


if __name__ == '__main__':
    import pprint

    search = county_clerk_search('Rama Avzi')
    # pprint.pprint(search)

    doc_ids = [x['doc_id'] for x in search]
    documents = [county_clerk_document(result) for result in doc_ids]

    pprint.pprint(documents)
