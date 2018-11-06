from flask import render_template, url_for, request, redirect, session, make_response
from flask_app import app, db, sheriff_sale, nj_parcels
from flask_app.forms import SaleDateForm
from flask_app.models import SheriffSale


@app.route("/", methods=['GET', 'POST'])
def home():
    form = SaleDateForm()

    if request.method == 'POST':
        return redirect(url_for('table_data', selected_date=form.sale_dates.data))
        # return redirect(url_for('test', data='Test'))
    return render_template('layout.html', form=form)


@app.route("/build_db", methods=['GET', 'POST'])
def build_database():
    form = SaleDateForm()

    import json

    with open('sheriff_sale_dump.json') as f:
        sheriff_sale_json = json.load(f)

        for data in sheriff_sale_json:
            sheriff_sale_data = SheriffSale(
                property_id=data['property_id'],
                sheriff=data['listing_details']['sheriff'],
                court_case=data['listing_details']['court_case'],
                sale_date=data['listing_details']['sale_date'],
                plaintiff=data['listing_details']['plaintiff'],
                defendant=data['listing_details']['defendant'],
                address=data['listing_details']['address'],
                priors=data['listing_details']['priors'],
                attorney=data['listing_details']['attorney'],
                judgment=data['listing_details']['judgment'],
                deed=data['listing_details']['deed'],
                deed_address=data['listing_details']['deed_address'],
                address_sanitized=data['sanitized']['address'],
                unit=data['sanitized']['unit'],
                city=data['sanitized']['city'],
                zip_code=data['sanitized']['zip_code'],
                maps_href=data['maps_href']
                # status_history=data[12]
            )
            db.session.add(sheriff_sale_data)
            db.session.commit()

    return render_template('layout.html', form=form)


@app.route("/table_data/<selected_date>", methods=['GET', 'POST'])
def table_data(selected_date):
    form = SaleDateForm()

    # date = selected_date.replace('-', '/')
    # if date[3] == '0':
    #     date = date[0:3] + date[4:]
    #
    # sale_date = SheriffSale.query.filter_by(sale_date=date).first()
    #
    # if sale_date:
    #     selected_data = SheriffSale.query.filter_by(sale_date=date).all()

    # else:
        # sheriff_sale_driver = sheriff_sale.build_dict()
    #
    #     selected_data = SheriffSale.query.filter_by(sale_date=date).all()
    #     return render_template('table_data.html',
    #                            sheriff_sale_data=selected_data,
    #                            form=form)
    #
    # return render_template('table_data.html',
    #                        sheriff_sale_data=selected_data,
    #                        form=form)

