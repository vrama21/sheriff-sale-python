from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from server import app, db
from ..models.sheriff_sale_model import SheriffSaleModel, StatusHistoryModel
from ..constants import CITY_LIST, COUNTY_LIST, NJ_DATA
from ..services.sheriff_sale.sheriff_sale import SheriffSale
from ..services.sheriff_sale.parse import parse
from ..services.nj_parcels.nj_parcels import NJParcels

# from ..services.county_clerk import *
# from ..services.zillow import test


@app.route("/api/home", methods=["GET", "POST"])
def home():
    counties = COUNTY_LIST
    cities = CITY_LIST
    nj_data = NJ_DATA

    sheriff_sale = SheriffSale("Atlantic")
    sale_dates = sheriff_sale.get_sale_dates()

    data = {
        "counties": counties,
        "cities": cities,
        "njData": nj_data,
        "saleDates": sale_dates,
    }

    return jsonify(data=data)


@app.route("/api/sheriff_sale", methods=["POST"])
def get_sheriff_sale_data():
    """
    Returns: Up to date values from the Sheriff Sale Scraper
    """
    county = request.get_json()["county"]
    sheriff_sale = SheriffSale(county)

    sale_dates = sheriff_sale.get_sale_dates()
    property_ids = sheriff_sale.get_property_ids()

    data = {"propertyIds": property_ids, "saleDates": sale_dates}

    return jsonify(data=data)


@app.route("/api/sheriff_sale/update_database", methods=["POST"])
def update_sheriff_sale_data():
    sheriff_sale = SheriffSale()
    county_list = sheriff_sale.get_counties()

    for county in county_list:
        print(f"Parsing Sheriff Sale Data for {county} County...")
        sheriff_sale = SheriffSale(county=county)
        sheriff_sale_listings_html = sheriff_sale.get_all_listing_details_tables()
        data = [
            parse(listing_html=listing_html, county=county)
            for listing_html in sheriff_sale_listings_html
        ]

        for listing in data:
            listing_details = listing["listing_details"]
            status_history = listing["status_history"]

            listing_exists = (
                db.session.query(SheriffSaleModel)
                .filter_by(address=listing_details["address"])
                .scalar()
                is not None
            )

            if not listing_exists:
                listing_to_insert = SheriffSaleModel(**listing_details)

                db.session.add(listing_to_insert)
                db.session.flush()
                db.session.refresh(listing_to_insert)

                for status in status_history:
                    status_history_to_insert = StatusHistoryModel(
                        sheriff_sale_id=listing_to_insert.id,
                        status=status["status"],
                        date=status["date"],
                    )

                    db.session.add(status_history_to_insert)

        db.session.commit()
        print(f"Parsing for {county} County has completed. ", '\n')

    return jsonify(data=data)


@app.route("/api/get_all_listings", methods=["GET"])
def get_all_listings():
    query = (
        db.session.query(SheriffSaleModel)
        .order_by(SheriffSaleModel.sale_date.desc())
        .filter_by(address="163 Tiffany Lane Willingboro Nj 08046")
        .all()
    )

    table_data = [data.serialize for data in query]

    return jsonify(data=table_data)


@app.route("/api/nj_parcels/get_static_data", methods=["GET"])
def nj_parcels_get_static_data():
    nj_parcels = NJParcels()

    counties = nj_parcels.get_county_list()
    cities = nj_parcels.get_city_list()

    data = {"cities": cities, "counties": counties}

    return jsonify(data=data)


@app.route("/api/nj_parcels/search", methods=["POST"])
def nj_parcels_search():
    nj_parcels = NJParcels()
    body = request.get_json()

    search = nj_parcels.search(address=body["address"], county=body["county"])

    return jsonify(data=search)


# @app.route('/api/zillow', methods=['GET'])
# def run_zillow():
#     _test = test()

#     return jsonify(data=t)


# @app.route('/api/county_clerk', methods=['GET', 'POST'])
# def county_clerk():
#     db.create_all()
#     db.session.commit()

#     mapping = doc_type_mapper()

#     search_results = county_clerk_search('Rama Avzi')

#     for result in search_results:
#         exists = db.session.query(
#             CountyClerkModel.doc_id).filter(CountyClerkModel.doc_id == result['doc_id']).first()
#         if not exists:
#             data = CountyClerkModel(**result)
#             db.session.add(data)

#     db.session.commit()

#     doc_ids = [x['doc_id'] for x in search_results]
#     documents = [county_clerk_document(result) for result in doc_ids]

#     data = {'search': search_results, 'documents': documents}

#     return jsonify(data=data)
