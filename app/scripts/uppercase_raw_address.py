# Upper case all listing.raw addresses in the database

from app import db
from app.models import Listing

all_listings = db.session.query(Listing).all()
for listing in all_listings:
    if listing.raw_address:
        listing.raw_address = (listing.raw_address).upper()

db.session.commit()
