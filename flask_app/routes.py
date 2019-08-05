from flask import render_template, url_for, request, redirect, session, make_response
from flask_app import app, db, sheriff_sale, nj_parcels
from flask_app.forms import SaleDateForm
from flask_app.models import SheriffSaleDB

from constants import BASE_DIR, FLASK_APP_DIR

import json
import os
import time
from urllib.parse import quote


@app.route("/", methods=['GET', 'POST'])
def home():
    form = SaleDateForm()

    db_path = FLASK_APP_DIR.joinpath('main.db')
    db_mod_date = time.ctime(os.path.getmtime(db_path))

    if request.method == 'POST':
        return redirect(url_for('table_data', selected_date=form.sale_date.data))

    return render_template('home.html', form=form, db_mod_date=db_mod_date)


@app.route("/update_database", methods=['POST'])
def build_database():
    # if not SheriffSaleDB.exists():

    if request.method == 'POST':

        sheriff_sale_data = sheriff_sale.sheriff_sale_dict()
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
                address_sanitized=row['sanitized']['address'],
                unit=row['sanitized']['unit'],
                city=row['sanitized']['city'],
                zip_code=row['sanitized']['zip_code'],
                maps_href=row['maps_url']
            )
            db.session.add(_sheriff_sale_data)
            db.session.commit()

        return render_template("home.html")

    else:
        return render_template("home.html")


@app.route("/table_data/<selected_date>", methods=['GET', 'POST'])
def table_data(selected_date):
    form = SaleDateForm()

    # Convert date to url format
    date = quote(selected_date)

    selected_data = SheriffSaleDB.query.filter_by(sale_date=date).all()
    results = SheriffSaleDB.query.filter_by(sale_date=date).count()

    # json_dumps_dir = BASE_DIR.joinpaths('json_dumps\\01_17_2019.json')
    # selected_data = json.loads(json_dumps_dir)

    return render_template('table_data.html',
                           sheriff_sale_data=selected_data,
                           form=form, results=results)
