from .. import db, scheduler
from ..models.sheriff_sale_model import SheriffSaleModel, StatusHistoryModel
from ..services.sheriff_sale import (
    SheriffSale,
    parse_listing_details,
    parse_status_history,
)


@scheduler.task('cron', id='daily_scrape_job', minute=30)
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

            for listing_html in sheriff_sale_listings_html:
                listing_details = parse_listing_details(listing_html, county)
                status_history = parse_status_history(listing_html, county)

                listing_exists = (
                    db.session.query(SheriffSaleModel)
                    .filter_by(address=listing_details['address'])
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
                            status=status['status'],
                            date=status['date'],
                        )

                        db.session.add(status_history_to_insert)

            db.session.commit()
            print(f'Parsing for {county} County has completed. ', '\n')
