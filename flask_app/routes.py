from flask import render_template, url_for, request, redirect, session
from flask_app import app, db, sheriff_sale, nj_parcels

# TODO: Figure out how to inherit the model from the init without importing it here.
# from database_models import SheriffSaleDB, NJParcelsDB


@app.route("/", methods=['GET', 'POST'])
def home():
    session['get_sale_dates'] = sheriff_sale.get_sale_dates()
    session['selected_sale_date'] = request.form.get('sale_dates')
    if request.method == 'POST':
        return redirect(url_for('table_data'))
    return render_template('layout.html', sale_dates=session['get_sale_dates'])


@app.route("/table_data", methods=['GET', 'POST'])
def table_data():
    # if request.method == 'GET':
    sheriff_sale_data = sheriff_sale.selenium_driver(session['selected_sale_date'])
    listing_details = sheriff_sale_data[0]
    google_maps_href_links = sheriff_sale_data[1]
    status_history = sheriff_sale_data[2]
    listing_dict = sheriff_sale.sheriff_sale_dict(listing_details)

    return render_template('table_data.html', sale_dates=session['get_sale_dates'],
                           listing_dict=listing_dict)
