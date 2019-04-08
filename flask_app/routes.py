from flask import render_template, url_for, request, redirect, session, make_response
from flask_app import app, db, sheriff_sale, nj_parcels
from flask_app.forms import SaleDateForm
from flask_app.models import SheriffSaleDB

import json
import os
import time
from urllib.parse import quote


@app.route("/", methods=['GET', 'POST'])
def home():
    form = SaleDateForm()

    # TODO: Use Pathlib instead
    cur_dir = os.getcwd()
    db_path = cur_dir + '\\flask_app\\main.db'
    db_mod_date = time.ctime(os.path.getmtime(db_path))

    if request.method == 'POST':
        return redirect(url_for('table_data', selected_date=form.sale_dates.data))

    return render_template('home.html', form=form, db_mod_date=db_mod_date)


@app.route("/database")
def update_database():
    form = SaleDateForm()

    return render_template('update_database.html', form=form)


@app.route("/update_database")
def build_database():
    form = SaleDateForm()

    if not SheriffSaleDB.exists():
        sheriff_sale_data = sheriff_sale.sheriff_sale_dict()
        for d in sheriff_sale_data:
            _sheriff_sale_data = SheriffSaleDB(
                sheriff=d['listing_details']['sheriff'],
                court_case=d['listing_details']['court_case'],
                sale_date=d['listing_details']['sale_date'],
                plaintiff=d['listing_details']['plaintiff'],
                defendant=d['listing_details']['defendant'],
                address=d['listing_details']['address'],
                priors=d['listing_details']['priors'],
                attorney=d['listing_details']['attorney'],
                judgment=d['listing_details']['judgment'],
                deed=d['listing_details']['deed'],
                deed_address=d['listing_details']['deed_address'],
                address_sanitized=d['sanitized']['address'],
                unit=d['sanitized']['unit'],
                city=d['sanitized']['city'],
                zip_code=d['sanitized']['zip_code'],
                maps_href=d['maps_url']
            )
            db.session.add(_sheriff_sale_data)
            db.session.commit()

    return render_template('home.html', form=form)


@app.route("/table_data/<selected_date>", methods=['GET', 'POST'])
def table_data(selected_date):
    form = SaleDateForm()

    # Convert date to url format
    date = quote(selected_date)

    # selected_data = SheriffSaleDB.query.filter_by(sale_date=date).all()
    # results = SheriffSaleDB.query.filter_by(sale_date=date).count()

    json_dumps_dir = r'F:\\Projects\\Sheriff_Sale\\json_dumps\\01_17_2019.json'
    selected_data = json.loads(json_dumps_dir)
    total_results = len(selected_data)
    return render_template('table_data.html',
                           sheriff_sale_data=selected_data,
                           form=form, results=total_results)

