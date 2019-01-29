import requests
from bs4 import BeautifulSoup


def requests_content(url, session=None):
    """ Creates a an html request session and returns the beautifulsoup parse"""
    s = session
    while session:
        response = s.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        return soup


def none_to_empty_string(match_object):
    """ Converts any Nones to an empty string in regex matches that occur in SheriffSale """
    for i, match in enumerate(match_object):
        if match:
            match_object[i] = match[0]
        else:
            match_object[i] = ""
    return match_object
