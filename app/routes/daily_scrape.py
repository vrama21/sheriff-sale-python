from flask import jsonify
from sqlalchemy import and_

from .. import db, scheduler
from ..constants import NJ_SHERIFF_SALE_COUNTIES
from ..models import Listing, StatusHistory
from ..services.sheriff_sale import SheriffSale
from . import main_bp


def check_if_listing_exists(listing) -> bool:
    listing_exists = (
        db.session.query(Listing)
        .filter(
            and_(
                Listing.court_case == listing.court_case,
                Listing.raw_address == listing.raw_address,
                Listing.sheriff_id == listing.sheriff_id,
            )
        )
        .first()
    ) is not None

    return listing_exists


@scheduler.task('cron', id='daily_scrape_job', day='*')
@main_bp.route('/api/daily_scrape', methods=['GET', 'POST'])
def daily_scrape():
    with scheduler.app.app_context():
        county_list = NJ_SHERIFF_SALE_COUNTIES

        for county in county_list:
            print(f'Parsing Sheriff Sale Data for {county} County...')
            sheriff_sale = SheriffSale(county=county)
            sheriff_sale_listings = sheriff_sale.get_listing_details_and_status_history(use_google_map_api=False)

            for sheriff_sale_listing in sheriff_sale_listings:
                listing = sheriff_sale_listing['listing']
                status_history = sheriff_sale_listing['status_history']

                listing_exists = check_if_listing_exists(listing)

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

                    print(f'Saved {len(status_history)} status histories for listing_id: {listing_to_insert.id}')

            db.session.commit()
            print(f'Parsing for {county} County has completed. ', '\n')

    return jsonify(message='daily scrape complete')
