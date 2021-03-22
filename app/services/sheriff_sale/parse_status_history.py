def parse_status_history(listing_html: str, county: str):
    """
    Parameters:
        listing_html (soup): A beautiful soup object to parse through
        county (str): The county that is being parsed

    Returns:
        A dictionary of parsed data points
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
