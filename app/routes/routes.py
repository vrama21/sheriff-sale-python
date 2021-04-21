import base64
import json
from flask import jsonify, request, Blueprint
from datetime import datetime

from .. import db, scheduler
from ..models import Listing, StatusHistory, CountyClerk
from ..constants import COUNTY_LIST, NJ_DATA, BUILD_DIR, CITIES_BY_COUNTY
from ..services.sheriff_sale import SheriffSale, parse_listing_details, parse_status_history
from ..services.sheriff_sale.parse_google_maps import get_coordinates_from_address
from ..services.nj_parcels.nj_parcels import NJParcels
from ..services.county_clerk import county_clerk_document, county_clerk_search


main_bp = Blueprint('main_bp', __name__, static_folder=str(BUILD_DIR), static_url_path='/home-static')


@main_bp.route('/')
def index():
    return main_bp.send_static_file('index.html')


@main_bp.route('/api/constants', methods=['GET'])
def home():
    cities_by_county = CITIES_BY_COUNTY

    sale_dates = [listing.sale_date for listing in db.session.query(Listing.sale_date).distinct()]
    sorted_sale_dates = sorted(sale_dates, key=lambda date: datetime.strptime(date, '%m/%d/%Y'), reverse=True)
    current_year = datetime.now().year
    clean_sale_dates = [sale_date for sale_date in sorted_sale_dates if sale_date[-4:] <= str(current_year)]

    data = {
        'counties': cities_by_county,
        'saleDates': clean_sale_dates,
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


@scheduler.task('cron', id='daily_scrape_job', day='*')
@main_bp.route('/api/daily_scrape', methods=['POST'])
def daily_scrape():
    county_list = [
        'Atlantic',
        'Bergen',
        'Burlington',
        'Camden',
        'Cumberland',
        'Essex',
        'Hudson',
        'Hunterdon',
        'Monmouth',
        'Morris',
        'Passaic',
        'Salem',
        'Union',
    ]

    with scheduler.app.app_context():
        for county in county_list:
            print(f'Parsing Sheriff Sale Data for {county} County...')
            sheriff_sale = SheriffSale(county=county)
            sheriff_sale_listings_html = sheriff_sale.get_all_listing_details_tables()

            listings_to_update = []

            for listing_html in sheriff_sale_listings_html:
                listing_details = parse_listing_details(listing_html, county)
                status_history = parse_status_history(listing_html)

                listing = db.session.query(Listing).filter_by(address=listing_details.get('address')).scalar()
                listing: dict = listing.serialize if listing else None
                listing_exists: bool = listing is not None

                # TODO: Move this to a separate update streets/cities route
                # if listing_exists:
                #     if (not listing.get('city') and listing_details.get('city')) or (
                #         not listing.get('street') and listing_details.get('street')
                #     ):
                #         print(f'Updating {listing.get("address")}...')
                #         listings_to_update.append({'id': listing['id'], **listing_details})

                if not listing_exists:
                    print(f'Inserting a new listing: {listing_details["address"]}')

                    formatted_address = f'{listing_details["street"]}, {listing_details["city"]}, NJ'
                    coordinates = get_coordinates_from_address(formatted_address)

                    if coordinates:
                        listing_details['latitude'] = coordinates['lat']
                        listing_details['longitude'] = coordinates['lng']

                    listing_to_insert = Listing(**listing_details)
                    db.session.add(listing_to_insert)
                    db.session.flush()
                    db.session.refresh(listing_to_insert)

                    for status in status_history:
                        status_history_to_insert = StatusHistory(
                            listing_id=listing_to_insert.id,
                            status=status.get('status'),
                            date=status.get('date'),
                        )

                        db.session.add(status_history_to_insert)

            if len(listings_to_update):
                db.session.bulk_update_mappings(Listing, listings_to_update)

            db.session.commit()
            print(f'Parsing for {county} County has completed. ', '\n')

    return jsonify(message='daily scrape complete')


@main_bp.route('/api/get_all_listings', methods=['GET'])
def get_all_listings():
    sheriff_sale_query = db.session.query(Listing).order_by(Listing.sale_date.desc()).all()

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


@main_bp.route('/api/county_clerk_doc_to_pdf', methods=['GET', 'POST'])
def county_clerk_doc_to_pdf():
    from base64 import b64decode
    import requests
    import codecs

    test_doc = {'ID': 5705275, 'convert': True, 'page': 1}
    response = requests.post(url='http://24.246.110.8/or_web1/api/document', data=test_doc)
    content = response.json()

    pdf_base64 = content['hi_res'].encode('utf-8')

    print(pdf_base64[0:10])
    bytes = base64.decodebytes(pdf_base64)
    # if bytes[0:4] != b'%PDF':
    #     raise ValueError('Missing the PDF file signature')

    with open('test.pdf', 'wb') as pdf:
        pdf.write(bytes)

    return jsonify(data=content)
