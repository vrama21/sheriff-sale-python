import re
import logging


def match_parser(regex, target, match_type, regexGroup=0, log=True):
    search = re.search(regex, target)
    if search:
        match = search.group(regexGroup).rstrip().title()

        return match
    else:
        if log:
            logging.error(f'{match_type} regex did not capture {target}')

        return None
