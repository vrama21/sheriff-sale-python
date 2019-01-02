from flask import render_template, url_for, request, redirect, session, make_response
from flask_app import app, db, sheriff_sale, nj_parcels
from flask_app.forms import SaleDateForm
from flask_app.models import SheriffSaleDB


@app.route("/", methods=['GET', 'POST'])
def home():
    form = SaleDateForm()

    if request.method == 'POST':
        return redirect(url_for('table_data', selected_date=form.sale_dates.data))
        # return redirect(url_for('test', data='Test'))
    return render_template('layout.html', form=form)


@app.route("/database")
def database():
    form = SaleDateForm()
    return render_template('database.html', form=form)


@app.route("/build_database", methods=['GET', 'POST'])
def build_database():
    form = SaleDateForm()

    # import json
    # with open('sheriff_sale_dump.json') as f:
    #     sheriff_sale_data = json.load(f)

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
    print(date)

    selected_data = SheriffSaleDB.query.filter_by(sale_date=date).all()
    results = SheriffSaleDB.query.filter_by(sale_date=date).count()
    print(selected_data)
    # sale_date = SheriffSale.query.filter_by(sale_date=date).first()
    #
    # if sale_date:

    # else:
        # sheriff_sale_driver = sheriff_sale.build_dict()
    #
    #     selected_data = SheriffSale.query.filter_by(sale_date=date).all()
    #     return render_template('table_data.html',
    #                            sheriff_sale_data=selected_data,
    #                            form=form)
    #
    return render_template('table_data.html',
                           sheriff_sale_data=selected_data,
                           form=form, results=results)

