import logging
import re


def match_parser(
    regex_pattern: re.Pattern,
    target: str,
    regex_name: str,
    regex_group: int = 0,
    log: bool = True,
) -> str | None:
    """
    Searches a regex matc

    :param regex_pattern: The regex pattern
    :param target: The string to perform the regex pattern on
    :param regex_name: The name of the regex
    :param regex_group: The regex group to return
    :param log: Whether to log errors for this parse

    :return: Returns a successful regex match or logs it if was unsuccessful
    """
    search = re.search(regex_pattern, target)
    if search:
        match = search.group(regex_group).rstrip().title()

        return match
    else:
        if log:
            logging.error(f'{regex_name} regex did not capture {target}')

        return None
