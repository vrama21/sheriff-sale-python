from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
from pathlib import Path
from ..utils import BASE_DIR


def test():
    path = Path(BASE_DIR, 'config/zillow_key.conf')
    with open(path, 'r') as f:
        key = f.readline().rstrip().replace("\n", "")

    print(key)
    zillow_data = ZillowWrapper(key)

    response = zillow_data.get_deep_search_results(address='574 Revere Way', zipcode='08205')
    # response = zillow_data.get_updated_property_details('37807220')
    result = GetDeepSearchResults(response)
    return result
