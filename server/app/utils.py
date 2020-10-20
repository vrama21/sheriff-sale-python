import json
from pathlib import Path
import pprint
import requests
from bs4 import BeautifulSoup
import re
import logging

pp = pprint.PrettyPrinter(indent=4)
BASE_DIR = Path(__file__).resolve().parent


def requests_content(url, session=None):
    """ Creates an html request session and returns the BeautifulSoup parse"""
    response = session.get(url) if session else requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    return soup


# TODO: May be deprecated
def none_to_empty_string(match_object):
    """ Converts any Nones to an empty string in regex matches that occur in SheriffSale """
    for i, match in enumerate(match_object):
        match_object[i] = match[0] if match else ""

    return match_object


def load_json_data(json_path):
    """
    Reads and loads a specified json file. The path arg follows the format of server/app/*json_path*
    """
    path = Path(BASE_DIR, json_path)

    with open(path, 'r') as file:
        json_data = json.load(file)

        return json_data


def match_parser(regex, target, type, regexGroup=0, log=True):
    search = re.search(regex, target)
    if search:
        match = search.group(regexGroup).rstrip().title()

        return match
    else:
        if log:
            logging.error(f'{type} regex did not capture {target}')

        return None
