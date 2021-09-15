from urllib.parse import urlencode

from app.services.sheriff_sale import SheriffSale, SheriffSaleListing

# sheriff_sale = SheriffSale(county='Atlantic', filter_out_sold_listings=False)
# parse = sheriff_sale.get_listing_details_and_status_history(use_google_map_api=False)
# print(parse)

sheriff_sale_listing = SheriffSaleListing(county='Atlantic', property_id='12345678', listing_html=None)
print(sheriff_sale_listing)
