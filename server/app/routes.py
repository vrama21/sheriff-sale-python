import os
import time
from pathlib import Path

from flask import (jsonify, request)

from . import app, db
from .models import SheriffSaleModel
from .constants import CITY_LIST, COUNTY_LIST, NJ_DATA
from .services.sheriff_sale.sheriff_sale import SheriffSale
from .services.nj_parcels.nj_parcels import NJParcels
from .services.county_clerk import *
from .services.zillow import test


@app.route('/api/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        db_path = Path(__file__).parent / 'main.db'
        db_mod_date = time.ctime(os.path.getmtime(db_path))

        counties = COUNTY_LIST
        cities = CITY_LIST
        nj_data = NJ_DATA

        sheriff_sale = SheriffSale('Atlantic')
        sale_dates = sheriff_sale.get_sale_dates()

        data = {
            'counties': counties,
            'cities': cities,
            'dbModDate': db_mod_date,
            'njData': nj_data,
            'saleDates': sale_dates
        }

        return jsonify(data=data, code=200)


@app.route('/api/sheriff_sale', methods=['POST'])
def get_sheriff_sale_data():
    """
    Returns:
         Up to date values from the Sheriff Sale Scraper
    """
    county = request.get_json()['county']
    sheriff_sale = SheriffSale(county=county)

    sale_dates = sheriff_sale.get_sale_dates()
    property_ids = sheriff_sale.get_property_ids()

    data = {
        'propertyIds': property_ids,
        'saleDates': sale_dates
    }

    return jsonify(data=data, code=200)


@app.route('/api/get_all_listings', methods=['GET'])
def get_all_listings():
    query = db.session\
        .query(SheriffSaleModel)\
        .order_by(SheriffSaleModel.sale_date.desc())\
        .all()

    table_data = [data.serialize for data in query]

    return jsonify(listings=table_data, code=200)


@app.route('/api/nj_parcels/get_static_data', methods=['GET'])
def nj_parcels_get_static_data():
    nj_parcels = NJParcels()

    counties = nj_parcels.get_county_list()
    cities = nj_parcels.get_city_list()

    data = {
        'cities': cities,
        'counties': counties
    }

    return jsonify(data=data, code=200)


@app.route('/api/nj_parcels/search', methods=['POST'])
def nj_parcels_search():
    nj_parcels = NJParcels()
    body = request.get_json()

    search = nj_parcels.search(address=body['address'], county=body['county'])

    return jsonify(data=search, code=200)


@app.route('/api/zillow', methods=['GET'])
def run_zillow():
    _test = test()

    return jsonify(data=t, code=200)


# @app.route('/api/update_database', methods=['GET', 'POST'])
# def update_database():
#     print('Running Sheriff_Sale parser and updating database...')

#     sheriff_sale = SheriffSale('Atlantic')
#     if request.method == 'GET':
#         sheriff_sale_data = sheriff_sale.main()

#         print({sheriff_sale_data})

#         for row in sheriff_sale_data:
#             _sheriff_sale_data = SheriffSaleModel(**row)
#             db.session.add(_sheriff_sale_data)

#         db.session.commit()

#         print('Sheriff Sale parser has completed...')

#         return jsonify(
#             message='success',
#             data=sheriff_sale_data,
#             code=200,
#         )

#     else:
#         return jsonify(message='failure', code=401)


# @app.route('/api/county_clerk', methods=['GET', 'POST'])
# def county_clerk():
#     db.create_all()
#     db.session.commit()

#     mapping = doc_type_mapper()

#     search_results = county_clerk_search('Rama Avzi')

#     for result in search_results:
#         exists = db.session.query(
#             CountyClerkModel.doc_id).filter(CountyClerkModel.doc_id == result['doc_id']).first()
#         if not exists:
#             data = CountyClerkModel(**result)
#             db.session.add(data)

#     db.session.commit()

#     doc_ids = [x['doc_id'] for x in search_results]
#     documents = [county_clerk_document(result) for result in doc_ids]

#     data = {'search': search_results, 'documents': documents}

#     return jsonify(data=data, code=200)
