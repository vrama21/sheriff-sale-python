from app import db
from app.models import Listing
from app.services.sheriff_sale import get_coordinates_from_address


listings = (
    db.session.query(Listing)
    .filter(Listing.latitude == None)
    .filter(Listing.longitude == None)
    .filter(Listing.street is not None)
    .filter(Listing.city is not None)
    .all()
)

for listing in listings:
    formatted_address = f'{listing.street}, {listing.city}, NJ'
    print(f'Adding address: {formatted_address} to be updated')

    coordinates = get_coordinates_from_address(formatted_address)

    if coordinates:
        print(f'Updating coordinates for address: {formatted_address}')

        listing.latitude = coordinates['lat']
        listing.longitude = coordinates['lng']

db.session.commit()

print('Script: update_coordinates has completed.')
