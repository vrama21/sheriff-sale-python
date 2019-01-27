from flask import render_template, url_for, request, redirect, session, make_response
from flask_app import app, db, sheriff_sale, nj_parcels
from flask_app.forms import SaleDateForm
from flask_app.models import SheriffSaleDB

import json
import os
import time


@app.route("/", methods=['GET', 'POST'])
def home():
    form = SaleDateForm()
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


@app.route("/build_database", methods=['GET', 'POST'])
def build_database():
    form = SaleDateForm()

    with open('sheriff_sale_dump.json') as f:
        sheriff_sale_data = json.load(f)

    sheriff_sale_data = sheriff_sale.sheriff_sale_dict()
    add = sheriff_sale.build_db(sheriff_sale_data, SheriffSaleDB)
    db.session.add(add)
    db.session.commit()

    return render_template('build_db.html', form=form)


@app.route("/table_data/<selected_date>", methods=['GET', 'POST'])
def table_data(selected_date):
    form = SaleDateForm()

    date = selected_date.replace('-', '/')
    if date[3] == '0':
        date = date[0:3] + date[4:]

    # selected_data = SheriffSaleDB.query.filter_by(sale_date=date).all()
    # results = SheriffSaleDB.query.filter_by(sale_date=date).count()

    json_dumps_dir = r'F:\\Projects\\Sheriff_Sale\\json_dumps\\01_17_2019.json'
    print(json_dumps_dir)
    selected_data = json.loads(json_dumps_dir)
    total_results = len(selected_data)
    return render_template('table_data.html',
                           sheriff_sale_data=selected_data,
                           form=form, results=total_results)

