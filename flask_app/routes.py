from flask import render_template, url_for, request, redirect, session, make_response
from flask_app import app, db, sheriff_sale, nj_parcels
from flask_app.forms import SearchFilter
from flask_app.models import SheriffSaleDB

from constants import BASE_DIR, FLASK_APP_DIR

import json
import os
import time
from urllib.parse import urlencode


@app.route("/", methods=["GET", "POST"])
def home():
    form = SearchFilter()

    db_path = FLASK_APP_DIR.joinpath("main.db")
    db_mod_date = time.ctime(os.path.getmtime(db_path))

    return render_template("home.html", form=form, db_mod_date=db_mod_date)


@app.route("/check_for_update")
def check_for_update(methods=["POST"]):
    sheriff_ids = tuple(sheriff_sale.get_sheriff_ids())
    print(len(sheriff_ids))

    db_sheriff_ids = SheriffSaleDB.query.filter(
        SheriffSaleDB.sheriff.in_(sheriff_ids)
    ).all()
    db_sheriff_ids_count = SheriffSaleDB.query.filter(
        SheriffSaleDB.sheriff.in_(sheriff_ids)
    ).count()
    print(db_sheriff_ids)
    print(db_sheriff_ids_count)

    return redirect(url_for("home"))


@app.route("/update_database")
def update_database(methods=["POST"]):
    sheriff_sale_data = sheriff_sale.sheriff_sale_dict()
    
    total = len(sheriff_sale_data)
    counter = 0

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
        counter += 1
        print(counter)
        db.session.add(_sheriff_sale_data)
        db.session.commit()

    return redirect(url_for("home"))


@app.route("/table_data", methods=["GET", "POST"])
def table_data():

    _query = SheriffSaleDB.query
    _county = request.args.get("county", None)
    _city = request.args.get("city", None)
    _sale_date = request.args.get("sale_date", None)

    if _county:
        _query = _query.filter(SheriffSaleDB.county == _county)
    if _city:
        _query = _query.filter(SheriffSaleDB.city == _city)
    if _sale_date:
        _query = _query.filter(SheriffSaleDB.sale_date == _sale_date)

    query = _query.order_by(SheriffSaleDB.city.asc()).all()
    results = _query.count()

    return render_template("table_data.html", query=query, results=results)
