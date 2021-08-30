from datetime import datetime

from flask import jsonify

from .. import db
from ..constants import CITIES_BY_COUNTY
from ..models import Listing
from . import main_bp


@main_bp.route('/api/get_constants', methods=['GET'])
def get_constants():
    cities_by_county = CITIES_BY_COUNTY

    sale_dates = [
        listing.sale_date for listing in db.session.query(Listing.sale_date).distinct() if listing.sale_date is not None
    ]
    sorted_sale_dates = sorted(sale_dates, key=lambda sale_date: datetime.strptime(sale_date, '%m/%d/%Y'))
    current_year = datetime.now().year
    clean_sale_dates = [
        sale_date for sale_date in sorted_sale_dates if datetime.strptime(sale_date, '%m/%d/%Y').year <= current_year
    ]

    data = {
        'counties': cities_by_county,
        'saleDates': clean_sale_dates,
    }

    return jsonify(data=data)
