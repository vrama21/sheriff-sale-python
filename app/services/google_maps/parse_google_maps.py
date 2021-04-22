from flask_googlemaps import get_address, get_coordinates
import os

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')


def get_coordinates_from_address(address):
    coordinates = None

    try:
        coordinates = get_coordinates(GOOGLE_MAPS_API_KEY, address)
    except IndexError:
        print(f'Could not get coordinates for address: {address}')

    return coordinates


def get_address_from_coordinates(lat, lng):
    address = get_address(GOOGLE_MAPS_API_KEY, lat, lng)

    return address
