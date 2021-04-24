class SheriffSaleStatusHistory:
    def __init__(self, listing_html):
        self.listing_html = listing_html

        self.status_history = None

    def parse_status_history_details(self):
        """
        Parses the status history table of a listings detail page
        """
        status_history_html = self.listing_html.find('table', id='longTable')

        status_history = []
        if status_history_html is not None:
            for tr in status_history_html.find_all('tr')[1:]:
                td = tr.find_all('td')
                listing_status = {
                    'status': td[0].text.strip(),
                    'date': td[1].text.strip(),
                }
                status_history.append(listing_status)

        self.status_history = status_history

    def parse(self):
        self.parse_status_history_details()

        return self.status_history
