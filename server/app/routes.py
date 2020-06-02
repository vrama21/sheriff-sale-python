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
from .settings import BASE_DIR
from .scrapers.sheriff_sale import SheriffSale


@app.route("/api/home", methods=["GET"])
def home():
    sheriff_sale = SheriffSale("15")

    db_path = Path(BASE_DIR, 'main.db')
    db_mod_date = time.ctime(os.path.getmtime(db_path))

    counties = COUNTY_LIST
    cities = CITY_LIST
    nj_data = NJ_DATA
    sale_dates = sheriff_sale.get_sale_dates()
    table_data = [data.serialize for data in SheriffSaleDB.query.all()]

    if request.method == "GET":
        return jsonify(
            dbModDate=db_mod_date,
            counties=counties,
            cities=cities,
            saleDates=sale_dates,
            njData=nj_data,
            tableData=table_data
        )


@app.route("/api/sheriff_sale")
def run_sheriff_sale(methods=["GET"]):
    sheriff_sale = SheriffSale("25")
    return jsonify("Success"), 200


@app.route("/api/check_for_update")
def check_for_update(methods=["POST"]):
    sheriff_sale = SheriffSale("15")

    # 1) Get the sheriff id's currently on the website
    sheriff_sale_ids_current = sheriff_sale.get_sheriff_ids()

    # 2) Query the db to get all the sheriff id's in the db
    sheriff_sale_ids_db = SheriffSaleDB.query.with_entities(
        SheriffSaleDB.sheriff).all()

    # 3) Check for any differences in between
    difference = list(set(sheriff_sale_ids_current) - set(sheriff_sale_ids_db))

    return jsonify(difference)


@app.route("/api/update_database")
def update_database(methods=["GET", "POST"]):
    sheriff_sale = SheriffSale("15")

    if request.method == "GET":
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
            "message": "Sheriff Sale Database Successfully Updated",
            "data": sheriff_sale_data,
        }), 200)

    else:
        return jsonify({'message': 'Updating the Sheriff Sale Database Failed'}), 401
