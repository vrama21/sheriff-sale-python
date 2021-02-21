import re
import logging


def match_parser(
    regex_pattern: re.Pattern,
    target: str,
    regex_name: str,
    regex_group: int = 0,
    log: bool = True,
):
    """
    Parameters:
        regex_pattern (re.Pattern): The regex pattern
        target (str): The string to perform the regex pattern on
        regex_name (str): The name of the regex
        regex_group (int): The regex group to return
        log (bool): Whether to log errors for this parse

    Returns:
        Returns a successful regex match or logs it if was unsuccessful
    """
    search = re.search(regex_pattern, target)
    if search:
        match = search.group(regex_group).rstrip().title()

        return match
    else:
        if log:
            logging.error(f'{regex_name} regex did not capture {target}')

        return None
