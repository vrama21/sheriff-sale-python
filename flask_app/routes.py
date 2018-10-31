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


@app.route("/table_data/<selected_date>", methods=['GET', 'POST'])
def table_data(selected_date):
    form = SaleDateForm()
    date = selected_date.replace('-', '/')
    # sale_date = SheriffSale.query.filter_by(sale_date=date).first()

    # if sale_date:
    #     sheriff_sale_data = SheriffSale.query.fetchall()
    # else:
    sheriff_sale_driver = sheriff_sale.selenium_driver(date)
    for key in sheriff_sale_driver.keys():
        for data in sheriff_sale_driver[key]:
            sheriff_sale_data = SheriffSale(
                                sheriff=data
                        # court_case=sheriff_sale_driver['court_case'],
                        # sale_date=sheriff_sale_driver['sale_date'],
                        # plaintiff=sheriff_sale_driver['plaintiff'],
                        # defendant=sheriff_sale_driver['defendant'],
                        # address=sheriff_sale_driver['address'],
                        # priors=sheriff_sale_driver['priors'],
                        # attorney=sheriff_sale_driver['attorney'],
                        # judgment=sheriff_sale_driver['judgment'],
                        # deed=sheriff_sale_driver['deed'],
                        # deed_address=sheriff_sale_driver['deed_address'],
                        # maps_href=sheriff_sale_driver['maps_href'],
                        # status_history=sheriff_sale_driver['status_history'],
                        # address_sanitized=sheriff_sale_driver['address_sanitized'],
                        # unit=sheriff_sale_driver['unit'],
                        # city=sheriff_sale_driver['city'],
                        # zip_code=sheriff_sale_driver['zip_code'],
        )
        db.session.add(sheriff_sale_data)
        db.session.commit()

    return render_template('table_data.html',
                           sheriff_sale_data=sheriff_sale_data,
                           form=form)


@app.route("/test/<data>")
def test(data):
    form = SaleDateForm()
    return render_template('about.html', form=form)
