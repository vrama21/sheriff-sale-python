import json
from pathlib import Path
import pprint
import requests
from bs4 import BeautifulSoup
import re
import logging


def requests_content(url, session=None):
    """ Creates an html request session and returns the BeautifulSoup parse"""
    response = session.get(url) if session else requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    return soup


def load_json_data(json_path):
    """
    Reads and loads a specified json file. The path arg follows the format of server/app/*json_path*
    """
    path = Path(__file__).resolve().parent / json_path

    with open(path, 'r') as file:
        json_data = json.load(file)

        return json_data
