import zillow
from pathlib import Path
from ..utils import BASE_DIR


def test():
    path = Path(BASE_DIR, 'config/zillow_key.conf')
    with open(path, 'r') as f:
        key = f.readline().replace("\n", "")

    api = zillow.ValuationApi()

    address = "574 Revere Way Galloway Township NJ"
    zip_code = "08205"

    data = api.GetSearchResults(key, address, zip_code)

