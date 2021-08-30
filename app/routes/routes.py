import base64
from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import and_

from .. import db, scheduler
from ..constants import BUILD_DIR, CITIES_BY_COUNTY, NJ_SHERIFF_SALE_COUNTIES
from ..models import Listing, StatusHistory
from ..services.county_clerk import county_clerk_document, county_clerk_search
from ..services.nj_parcels.nj_parcels import NJParcels
from ..services.sheriff_sale import SheriffSale, SheriffSaleListing

main_bp = Blueprint('main_bp', __name__, static_folder=str(BUILD_DIR), static_url_path='/home-static')


@main_bp.route('/api/get_listing/<int:id>', methods=['GET'])
def get_listing(id):
    listing = (db.session.query(Listing).filter_by(id=id).one()).serialize

    return jsonify(data=listing)


@main_bp.route('/api/nj_parcels/search', methods=['POST'])
def nj_parcels_search():
    nj_parcels = NJParcels()
    body = request.get_json()

    search = nj_parcels.search(address=body['address'], county=body['county'])

    return jsonify(data=search)


@main_bp.route('/api/county_clerk', methods=['GET', 'POST'])
def county_clerk():
    search_results = county_clerk_search('Rama Avzi')
    # for result in search_results:
    #     # print('\n')
    #     for k, v in result.items():
    #         print(k, v, type(v))
    #     print('\n')

    # for result in search_results:
    #     exists = (
    #         db.session.query(CountyClerkModel.doc_id)
    #         .filter(CountyClerkModel.doc_id == result['doc_id'])
    #         .first()
    #     )
    #     # if not exists:
    #     #     data = CountyClerkModel(**result)
    #     #     db.session.add(data)

    # db.session.commit()

    doc_ids = [x['doc_id'] for x in search_results]
    documents = [county_clerk_document(result) for result in doc_ids]

    data = {'search': search_results, 'documents': documents}

    return jsonify(data=data)


@main_bp.route('/api/county_clerk_doc_to_pdf', methods=['GET', 'POST'])
def county_clerk_doc_to_pdf():
    import codecs
    from base64 import b64decode

    import requests

    test_doc = {'ID': 5705275, 'convert': True, 'page': 1}
    response = requests.post(url='http://24.246.110.8/or_web1/api/document', data=test_doc)
    content = response.json()

    pdf_base64 = content['hi_res'].encode('utf-8')

    print(pdf_base64[0:10])
    bytes = base64.decodebytes(pdf_base64)
    # if bytes[0:4] != b'%PDF':
    #     raise ValueError('Missing the PDF file signature')

    with open('test.pdf', 'wb') as pdf:
        pdf.write(bytes)

    return jsonify(data=content)
