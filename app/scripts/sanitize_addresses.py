import re

from app import db
from app.models import Listing
from app.utils import match_parser
from app.services.sheriff_sale import SheriffSaleListing


all_listings = db.session.query(Listing).all()
unit_listings = db.session.query(Listing).filter(Listing.address.like('%Unit%'))

regex_unit = re.compile(r'(Unit|Apt).([0-9A-Za-z-]+)')

for listing in all_listings:
    # Updates State in Address
    if listing.address and 'Nj' in listing.address:
        updated_address = listing.address.replace('Nj', 'NJ')
        print(f'\nUpdating address...\nfrom: {listing.address}\nto:   {updated_address}')
        listing.address = updated_address

for listing in unit_listings:
    if listing.address:
        updated_address = listing.address.replace('No. ', '')
        print(f'\nUpdating address...\nfrom: {listing.address}\nto: {updated_address}')
        listing.address = updated_address

    unit_match = match_parser(regex_unit, target=listing.address, regex_name='unit', log=False)
    if unit_match:
        print(f'\nUpdating unit...\nfrom: {listing.unit}\nto: {unit_match}')
        listing.unit = unit_match

db.session.commit()
