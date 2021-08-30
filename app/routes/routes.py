import base64
from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import and_

from .. import db, scheduler
from ..constants import BUILD_DIR, CITIES_BY_COUNTY, NJ_SHERIFF_SALE_COUNTIES
from ..models import Listing, StatusHistory
from ..services.county_clerk import county_clerk_document, county_clerk_search
from ..services.nj_parcels.nj_parcels import NJParcels
from ..services.sheriff_sale import SheriffSale, SheriffSaleListing

main_bp = Blueprint('main_bp', __name__, static_folder=str(BUILD_DIR), static_url_path='/home-static')


@main_bp.route('/')
def index():
    return main_bp.send_static_file('index.html')


@main_bp.route('/api/constants', methods=['GET'])
def home():
    cities_by_county = CITIES_BY_COUNTY

    sale_dates = [
        listing.sale_date for listing in db.session.query(Listing.sale_date).distinct() if listing.sale_date is not None
    ]
    sorted_sale_dates = sorted(sale_dates, key=lambda sale_date: datetime.strptime(sale_date, '%m/%d/%Y'))
    current_year = datetime.now().year
    clean_sale_dates = [
        sale_date for sale_date in sorted_sale_dates if datetime.strptime(sale_date, '%m/%d/%Y').year <= current_year
    ]

    data = {
        'counties': cities_by_county,
        'saleDates': clean_sale_dates,
    }

    return jsonify(data=data)


@scheduler.task('cron', id='daily_scrape_job', day='*')
@main_bp.route('/api/daily_scrape', methods=['GET', 'POST'])
def daily_scrape():
    county_list = NJ_SHERIFF_SALE_COUNTIES

    with scheduler.app.app_context():
        for county in county_list:
            print(f'Parsing Sheriff Sale Data for {county} County...')
            sheriff_sale = SheriffSale(county=county)
            sheriff_sale_listings = sheriff_sale.get_listing_details_and_status_history(use_google_map_api=False)

            for sheriff_sale_listing in sheriff_sale_listings:
                print(sheriff_sale_listing)
                listing = sheriff_sale_listing['listing']
                status_history = sheriff_sale_listing['status_history']

                listing_exists = (
                    db.session.query(Listing)
                    .filter(
                        and_(
                            Listing.sheriff_id == listing.sheriff_id,
                            Listing.court_case == listing.court_case,
                        )
                    )
                    .first()
                ) is not None

                if listing_exists:
                    print(listing.address, listing.raw_address)
                    print(f'{listing.raw_address} already exists...')
                else:
                    print(f'Saving a new listing: {listing.raw_address}...')

                    listing_to_insert = Listing(**listing.__dict__())
                    db.session.add(listing_to_insert)
                    db.session.flush()
                    db.session.refresh(listing_to_insert)

                    print(f'Saved new listing: ${listing_to_insert.id}')

                    for status in status_history:
                        status_history_to_insert = StatusHistory(
                            listing_id=listing_to_insert.id,
                            status=status.get('status'),
                            date=status.get('date'),
                        )

                        db.session.add(status_history_to_insert)

                    print(
                        f'Saved {len(status_history)} instances of status_history for listing_id: {listing_to_insert.id}'
                    )

            db.session.commit()
            print(f'Parsing for {county} County has completed. ', '\n')

    return jsonify(message='daily scrape complete')


@main_bp.route('/api/get_all_listings', methods=['GET'])
def get_all_listings():
    all_listings = db.session.query(Listing).all()

    all_listings = [data.serialize for data in all_listings]

    return jsonify(data=all_listings)


@main_bp.route('/api/get_listing/<int:id>', methods=['GET'])
def get_listing(id):
    listing = (db.session.query(Listing).filter_by(id=id).one()).serialize

    return jsonify(data=listing)


@main_bp.route('/api/nj_parcels/search', methods=['POST'])
def nj_parcels_search():
    nj_parcels = NJParcels()
    body = request.get_json()

    search = nj_parcels.search(address=body['address'], county=body['county'])

    return jsonify(data=search)


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
    import codecs
    from base64 import b64decode

    import requests

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
