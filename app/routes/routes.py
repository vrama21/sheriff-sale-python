from flask import jsonify, request, Blueprint

from .. import db
from ..models import SheriffSaleModel, CountyClerkModel
from ..constants import CITY_LIST, COUNTY_LIST, NJ_DATA, BUILD_DIR
from ..services.sheriff_sale import SheriffSale
from ..services.nj_parcels.nj_parcels import NJParcels
from ..services.county_clerk import county_clerk_document, county_clerk_search


main_bp = Blueprint(
    'main_bp', __name__, static_folder=str(BUILD_DIR), static_url_path='/home-static'
)


@main_bp.route('/')
def index():
    return main_bp.send_static_file('index.html')


@main_bp.route('/api/constants', methods=['GET', 'POST'])
def home():
    counties = COUNTY_LIST
    cities = CITY_LIST
    nj_data = NJ_DATA

    data = {
        'counties': counties,
        'cities': cities,
        'njData': nj_data,
    }

    return jsonify(data=data)


@main_bp.route('/api/sheriff_sale', methods=['POST'])
def get_sheriff_sale_data():
    """
    Returns:
         Up to date values from the Sheriff Sale Scraper
    """
    county = request.get_json()['county']
    sheriff_sale = SheriffSale(county)

    sale_dates = sheriff_sale.get_sale_dates()
    property_ids = sheriff_sale.get_property_ids()

    data = {'propertyIds': property_ids, 'saleDates': sale_dates}

    return jsonify(data=data)


@main_bp.route('/api/get_all_listings', methods=['GET'])
def get_all_listings():
    sheriff_sale_query = (
        db.session.query(SheriffSaleModel)
        .order_by(SheriffSaleModel.sale_date.desc())
        .all()
    )

    sheriff_sale_query = [data.serialize for data in sheriff_sale_query]

    return jsonify(data=sheriff_sale_query)


@main_bp.route('/api/nj_parcels/get_static_data', methods=['GET'])
def nj_parcels_get_static_data():
    nj_parcels = NJParcels()

    counties = nj_parcels.get_county_list()
    cities = nj_parcels.get_city_list()

    data = {'cities': cities, 'counties': counties}

    return jsonify(data=data)


@main_bp.route('/api/nj_parcels/search', methods=['POST'])
def nj_parcels_search():
    nj_parcels = NJParcels()
    body = request.get_json()

    search = nj_parcels.search(address=body['address'], county=body['county'])

    return jsonify(data=search)


# @main.route('/api/zillow', methods=['GET'])
# def run_zillow():
#     _test = test()

#     return jsonify(data=t)


@main_bp.route('/api/county_clerk', methods=['GET', 'POST'])
def county_clerk():
    search_results = county_clerk_search('Rama Avzi')
    # for result in search_results:
    #     # print('\n')
    #     for k, v in result.items():
    #         print(k, v, type(v))
    #     print('\n')

    # for result in search_results:
    #     exists = (
    #         db.session.query(CountyClerkModel.doc_id)
    #         .filter(CountyClerkModel.doc_id == result['doc_id'])
    #         .first()
    #     )
    #     # if not exists:
    #     #     data = CountyClerkModel(**result)
    #     #     db.session.add(data)

    # db.session.commit()

    doc_ids = [x['doc_id'] for x in search_results]
    documents = [county_clerk_document(result) for result in doc_ids]

    data = {'search': search_results, 'documents': documents}

    return jsonify(data=data)
