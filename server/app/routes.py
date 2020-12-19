import json
import os
import time
from pathlib import Path
from urllib.parse import urlencode

from flask import (jsonify, make_response, redirect, render_template, request, session, url_for)
from flask_sqlalchemy import SQLAlchemy

from . import app, db
from .models import SheriffSaleModel, CountyClerkModel, NJParcelsModel
from .constants import CITY_LIST, COUNTY_LIST, NJ_DATA
from .utils import load_json_data
from .services.sheriff_sale.sheriff_sale import SheriffSale
from .services.nj_parcels import NJParcels
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


@app.route('/api/listings', methods=['GET'])
def getAllListings():
    query = db.session\
        .query(SheriffSaleModel)\
        .join(NJParcelsModel)\
        .order_by(SheriffSaleModel.sale_date.desc())\
        .all()
    # query = db.session.query(SheriffSaleModel).join(SheriffSaleModel, NJParcelsModel).all()
    # print(query)
    table_data = [data.serialize for data in query]
    return jsonify(listings=table_data, code=200)


@app.route('/api/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        data = request.get_json()
        body = data['body']
        data1 = data['body']
        print(data1)
        return jsonify(data=body, code=200)


@app.route('/api/sheriff_sale', methods=['GET', 'POST'])
def run_sheriff_sale():
    if request.method == 'POST':
        try:
            county = request.get_json()['county']
            sheriff_sale = SheriffSale(county)
            response = sheriff_sale.get_table_data()

            return jsonify(data=response, code=200)
        except TypeError as error:
            return jsonify(message=error, code=401)


@app.route('/api/nj_parcels', methods=['GET'])
def run_nj_parcels():
    nj_parcels = NJParcels()

    atlantic = {'Atlantic': '25'}
    sheriff_sale = SheriffSale(atlantic)

    data = sheriff_sale.get_table_data()[2]

    address = data['address']['street']
    property_links = nj_parcels.get_property_parameters(address)
    taxes = nj_parcels.get_property_taxes(property_links['cityBlockLot'])

    data['njParcels'] = property_links
    data.update(taxes)

    return jsonify(data=data, code=200)


@app.route('/api/zillow', methods=['GET'])
def run_zillow():
    t = test()

    return jsonify(data=t, code=200)


@app.route('/api/update_database', methods=['GET', 'POST'])
def update_database():
    print('Running Sheriff_Sale parser and updating database...')
    sheriff_sale = SheriffSale('Atlantic')
    if request.method == 'GET':
        sheriff_sale_data = sheriff_sale.main()

        for row in sheriff_sale_data:
            _sheriff_sale_data = SheriffSaleModel(**row)
            db.session.add(_sheriff_sale_data)

        db.session.commit()

        return jsonify(
            message='Sheriff Sale Database Successfully Updated',
            data=sheriff_sale_data,
            code=200,
        )

    else:
        return jsonify(message='Updating the Sheriff Sale Database Failed', code=401)


@app.route('/api/county_clerk', methods=['GET', 'POST'])
def county_clerk():
    db.create_all()
    db.session.commit()

    mapping = doc_type_mapper()

    search_results = county_clerk_search('Rama Avzi')

    for result in search_results:
        exists = db.session.query(CountyClerkModel.doc_id).filter(CountyClerkModel.doc_id == result['doc_id']).first()
        if not exists:
            data = CountyClerkModel(**result)
            db.session.add(data)

    db.session.commit()

    doc_ids = [x['doc_id'] for x in search_results]
    documents = [county_clerk_document(result) for result in doc_ids]

    data = {'search': search_results, 'documents': documents}

    return jsonify(data=data, code=200)
