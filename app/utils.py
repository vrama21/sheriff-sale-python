import json
import logging
import regex
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def requests_content(url: str, method: str, session: requests.Session = None, cookies=None, data=None):
    """
    Creates an html request session and returns the BeautifulSoup parse

    Parameters:
        url: The url to fetch the request from
        session: If a session already exists, update the request in the current session

    Returns:
        A beautifulsoup object of the request
    """
    requests_session = session or requests
    response = None

    try:
        if method == 'GET':
            response = requests_session.get(url, cookies=cookies, data=data)

        elif method == 'POST':
            response = requests_session.post(url, cookies=cookies, data=data)

    except ConnectionError as err:
        raise ConnectionError('Cannot Access URL: ', err)

    if response:
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        return soup


def load_json_data(json_path: str):
    """
    Reads and loads a specified json file.

    Parameters:
        json_path: The path arg follows the format of app/*json_path*

    Returns:
        A json object
    """

    path = Path(__file__).resolve().parent / json_path

    with open(path, 'r') as file:
        json_data = json.load(file)

        return json_data


def get_class_attributes(class_instance, custom_attributes_only=True):
    attributes = (
        [a for a in dir(class_instance) if not a.startswith('__')]
        if custom_attributes_only
        else [a for a in dir(class_instance)]
    )

    return attributes


def get_class_attributes_and_values(class_instance):
    attributes = get_class_attributes(class_instance)

    attribute_values = {attribute: getattr(class_instance, attribute) for attribute in attributes}

    return attribute_values


def match_parser(
    regex_pattern: regex.Pattern,
    target: str,
    regex_name: str,
    regex_group: int = 0,
    log: bool = True,
):
    """
    Searches a regex match

    :param regex_pattern: The regex pattern
    :param target: The string to perform the regex pattern on
    :param regex_name: The name of the regex
    :param regex_group: The regex group to return
    :param log: Whether to log errors for this parse

    :return: Returns a successful regex match or logs it if was unsuccessful
    """
    if not target:
        logging.error(f'{target} is null')
        return None

    search = regex.search(regex_pattern, target.upper())
    if search:
        match = search.group(regex_group).rstrip().title()

        return match

    if log:
        logging.error(f'{regex_name} regex did not capture {target}')

    return None
