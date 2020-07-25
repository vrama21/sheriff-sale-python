import json
import os
import time
from pathlib import Path
from urllib.parse import urlencode

from flask import (jsonify, make_response, redirect, render_template, request,
                   session, url_for)

from . import app, db
from .models import SheriffSaleDB
from .constants import CITY_LIST, COUNTY_LIST, NJ_DATA
from .utils import BASE_DIR
from .scrapers.sheriff_sale import SheriffSale
from .scrapers.nj_parcels import NJParcels
from .scrapers.zillow import test


@app.route('/api/home', methods=['GET'])
def home():
    sheriff_sale = SheriffSale({'Atlantic': '15'})

    db_path = Path(BASE_DIR, 'main.db')
    db_mod_date = time.ctime(os.path.getmtime(db_path))

    counties = COUNTY_LIST
    cities = CITY_LIST
    nj_data = NJ_DATA
    sale_dates = sheriff_sale.get_sale_dates()
    table_data = [data.serialize for data in SheriffSaleDB.query.all()]

    if request.method == 'GET':
        return jsonify(dbModDate=db_mod_date,
                       counties=counties,
                       cities=cities,
                       saleDates=sale_dates,
                       njData=nj_data,
                       tableData=table_data)


@app.route('/api/search')
def search(methods=['GET', 'POST']):
    if request.method == 'GET':
        print('GET')
        return request.data, 200
    elif request.method == 'POST':
        print('Test')
        print(request)
        print(request.data)
        return request.data, 200


@app.route('/api/sheriff_sale')
def run_sheriff_sale(methods=['GET']):
    atlantic = {'Atlantic': '25'}
    camden = {'Camden': '1'}
    sheriff_sale = SheriffSale(atlantic)
    response = sheriff_sale.get_table_data()
    return jsonify(response), 200


@app.route('/api/nj_parcels')
def run_nj_parcels(methods=['GET']):
    nj_parcels = NJParcels()

    atlantic = {'Atlantic': '25'}
    sheriff_sale = SheriffSale(atlantic)

    data = sheriff_sale.get_table_data()[2]

    address = data['address']['street']
    property_links = nj_parcels.get_property_parameters(address)
    taxes = nj_parcels.get_property_taxes(property_links['cityBlockLot'])

    data['njParcels'] = property_links
    data.update(taxes)

    return jsonify(data), 200


@app.route('/api/zillow')
def run_zillow(methods=['GET']):
    t = test()

    return jsonify(t), 200


@app.route('/api/update_database')
def update_database(methods=['GET', 'POST']):
    sheriff_sale = SheriffSale('15')
    if request.method == 'GET':
        sheriff_sale_data = sheriff_sale.main()

        for row in sheriff_sale_data:
            _sheriff_sale_data = SheriffSaleDB(
                sheriff=row.listing_details.sheriff,
                court_case=row.listing_details.court_case,
                sale_date=row.listing_details.sale_date,
                plaintiff=row.listing_details.plaintiff,
                defendant=row.listing_details.defendant,
                address=row.listing_details.address,
                priors=row.listing_details.priors,
                attorney=row.listing_details.attorney,
                judgment=row.listing_details.judgment,
                deed=row.listing_details.deed,
                deed_address=row.listing_details.deed_address,
                maps_url=row.maps_url,
                address_sanitized=row.sanitized.address,
                unit=row.sanitized.unit,
                secondary_unit=row.sanitized.secondary_unit,
                city=row.sanitized.city,
                zip_code=row.sanitized.zip_code,
            )
            db.session.add(_sheriff_sale_data)
            db.session.commit()

        return (jsonify({
            'message': 'Sheriff Sale Database Successfully Updated',
            'data': sheriff_sale_data,
        }), 200)

    else:
        return jsonify(
            {'message': 'Updating the Sheriff Sale Database Failed'}), 401
