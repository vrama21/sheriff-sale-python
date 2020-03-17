import json
import requests
from bs4 import BeautifulSoup
from pathlib import PurePath, Path
from settings import FLASK_APP_DIR

def requests_content(url, session=None):
    """ Creates a an html request session and returns the BeautifulSoup parse"""
    s = session
    while session:
        response = s.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        return soup


# TODO: May be deprecated
def none_to_empty_string(match_object):
    """ Converts any Nones to an empty string in regex matches that occur in SheriffSale """
    for i, match in enumerate(match_object):
        if match:
            match_object[i] = match[0]
        else:
            match_object[i] = ""
    return match_object


def load_json_data(json_file):
    path = PurePath(FLASK_APP_DIR, 'scrapers/json', json_file)
    with open (path, 'r') as f:
        json_data = json.load(f)
        return json_data
