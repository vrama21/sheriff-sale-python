from flask import Blueprint
from ..constants import BUILD_DIR

main_bp = Blueprint('main_bp', __name__, static_folder=str(BUILD_DIR), static_url_path='/home-static')


@main_bp.route('/')
def index():
    return main_bp.send_static_file('index.html')


from .daily_scrape import daily_scrape
from .get_all_listings import get_all_listings
from .get_constants import get_constants
