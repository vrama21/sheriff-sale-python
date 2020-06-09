import json
from pathlib import Path
import pprint
import requests
from bs4 import BeautifulSoup
import re
import logging

from .settings import BASE_DIR

pp = pprint.PrettyPrinter(indent=4)


def requests_content(url, session=None):
    """ Creates an html request session and returns the BeautifulSoup parse"""
    response = None
    if session:
        response = session.get(url)
    else:
        response = requests.get(url)

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


def load_json_data(json_path):
    """
    Reads and loads a specified json file. The path arg follows the format of server/app/*json_path*
    """
    path = Path(BASE_DIR, json_path)
    with open(path, 'r') as file:
        json_data = json.load(file)
        return json_data


def match_parser(regex, target, regexGroup=0, log=True):
    try:
        match = re.search(regex, target).group(regexGroup).rstrip().title()
        return match
    except AttributeError as err:
        if log:
            logging.error(f'{err} - {target}')
        return None
