from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity

from .. import db
from ..models import Listing
from . import main_bp


@main_bp.route('/api/get_all_listings', methods=['GET'])
@jwt_required()
def get_all_listings():
    print(get_jwt_identity())
    all_listings = db.session.query(Listing).all()

    all_listings = [data.serialize for data in all_listings]

    return jsonify(data=all_listings)
