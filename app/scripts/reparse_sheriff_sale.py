# Parses NJ sheriff sale website and updates listing table with new/missing data
from sqlalchemy import and_

from app import db
from app.constants import NJ_SHERIFF_SALE_COUNTIES
from app.models import Listing
from app.services.sheriff_sale import (SheriffSale, SheriffSaleListing,
                                       SheriffSaleStatusHistory)

county_list = NJ_SHERIFF_SALE_COUNTIES

for county in county_list:
    print(f'Parsing Sheriff Sale Data for {county} County...')
    sheriff_sale = SheriffSale(county=county, filter_out_sold_listings=True)
    sheriff_sale_listings = sheriff_sale.get_listing_details_and_status_history(use_google_map_api=False)

    for sheriff_sale_listing in sheriff_sale_listings:
        parsed_listing: SheriffSaleListing = sheriff_sale_listing['listing']
        status_history: SheriffSaleStatusHistory = sheriff_sale_listing['status_history']

        db_listing = (
            db.session.query(Listing)
            .filter(
                and_(
                    Listing.sheriff_id == parsed_listing.sheriff_id,
                    Listing.court_case == parsed_listing.court_case,
                )
            )
            .first()
        )

        if db_listing:
            print(f'Updating listing_id {db_listing.id}')

            for key, value in parsed_listing.__dict__().items():
                setattr(db_listing, key, value)

    db.session.commit()
