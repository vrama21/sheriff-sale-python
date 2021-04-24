# Update raw_address to its original state

from sqlalchemy import and_

from app import db
from app.constants import NJ_SHERIFF_SALE_COUNTIES
from app.models import Listing
from app.services.sheriff_sale import SheriffSale


county_list = NJ_SHERIFF_SALE_COUNTIES

for county in county_list:
    print(f'Parsing Sheriff Sale Data for {county} County...')
    sheriff_sale = SheriffSale(county=county)
    sheriff_sale_listings = sheriff_sale.get_listing_details_and_status_history(use_google_map_api=False)

    for sheriff_sale_listing in sheriff_sale_listings:
        listing = sheriff_sale_listing['listing']
        status_history = sheriff_sale_listing['status_history']

        db_listing = (
            db.session.query(Listing)
            .filter(
                and_(
                    Listing.sheriff_id == listing.sheriff_id,
                    Listing.court_case == listing.court_case,
                )
            )
            .first()
        )

        if db_listing:
            print(f'Updating listing: {db_listing.raw_address} to {listing.raw_address}')

            db_listing.raw_address = listing.raw_address

    db.session.commit()
