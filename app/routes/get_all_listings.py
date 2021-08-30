from flask import jsonify

from .. import db
from ..models import Listing
from . import main_bp


@main_bp.route('/api/get_all_listings', methods=['GET'])
def get_all_listings():
    all_listings = db.session.query(Listing).all()

    all_listings = [data.serialize for data in all_listings]

    return jsonify(data=all_listings)
