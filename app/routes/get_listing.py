from flask import jsonify

from .. import db
from ..models import Listing
from . import main_bp


@main_bp.route('/api/get_listing/<int:id>', methods=['GET'])
def get_listing(id):
    listing = (db.session.query(Listing).filter_by(id=id).one()).serialize

    return jsonify(data=listing)
