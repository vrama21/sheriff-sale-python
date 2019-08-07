from flask import render_template, url_for, request, redirect, session, make_response
from flask_app import app, db, sheriff_sale, nj_parcels
from flask_app.forms import SaleDateForm
from flask_app.models import SheriffSaleDB

from constants import BASE_DIR, FLASK_APP_DIR

import json
import os
import time
from urllib.parse import quote, unquote


@app.route("/", methods=['GET', 'POST'])
def home():
    form = SaleDateForm()

    db_path = FLASK_APP_DIR.joinpath('main.db')
    db_mod_date = time.ctime(os.path.getmtime(db_path))

    if request.method == 'POST':
        return redirect(url_for('table_data', selected_date=form.sale_date.data))

    return render_template('home.html', form=form, db_mod_date=db_mod_date)


@app.route("/check_for_update")
def check_for_update(methods=["POST"]):
    sheriff_ids = sheriff_sale.get_sheriff_ids()    
    db_sheriff_ids = SheriffSaleDB.query.filter_by(sheriff=sheriff_ids)
    print(sheriff_ids)
    print(db_sheriff_ids)


@app.route("/update_database")
def update_database(methods=['POST']):
    # if request.method == 'POST':

    sheriff_sale_data = sheriff_sale.sheriff_sale_dict()
    print(sheriff_sale_data)
    for row in sheriff_sale_data:
        _sheriff_sale_data = SheriffSaleDB(
            sheriff=row['listing_details']['sheriff'],
            court_case=row['listing_details']['court_case'],
            sale_date=row['listing_details']['sale_date'],
            plaintiff=row['listing_details']['plaintiff'],
            defendant=row['listing_details']['defendant'],
            address=row['listing_details']['address'],
            priors=row['listing_details']['priors'],
            attorney=row['listing_details']['attorney'],
            judgment=row['listing_details']['judgment'],
            deed=row['listing_details']['deed'],
            deed_address=row['listing_details']['deed_address'],
            maps_url=row['maps_url'],
            address_sanitized=row['sanitized']['address'],
            unit=row['sanitized']['unit'],
            secondary_unit=row['sanitized']['secondary_unit'],
            city=row['sanitized']['city'],
            zip_code=row['sanitized']['zip_code']
        )
        db.session.add(_sheriff_sale_data)
        db.session.commit()

    return redirect(url_for('home'))

    # else:
    #     return render_template("home.html")


@app.route("/table_data/<selected_date>", methods=['GET', 'POST'])
def table_data(selected_date):
    form = SaleDateForm()

    selected_data = SheriffSaleDB.query.filter_by(sale_date=selected_date).all()
    results = SheriffSaleDB.query.filter_by(sale_date=selected_date).count()

    if request.method == 'POST':
        return redirect(url_for('table_data', selected_date=form.sale_date.data))

    return render_template('table_data.html',
                           sheriff_sale_data=selected_data,
                           form=form, results=results)
