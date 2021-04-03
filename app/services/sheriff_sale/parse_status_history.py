import bs4


def parse_status_history(listing_html: bs4.element.Tag) -> list:
    """
    Parses the status history table of a listings detail page

    :param listing_html: A beautiful soup object to parse through

    :return: A list of status history data points
    """
    status_history_html = listing_html.find('table', id='longTable')

    status_history = []
    if status_history_html is not None:
        for tr in status_history_html.find_all('tr')[1:]:
            td = tr.find_all('td')
            listing_status = {
                'status': td[0].text.strip(),
                'date': td[1].text.strip(),
            }
            status_history.append(listing_status)

    return status_history
