import logging
import re
import requests

from ...utils import requests_content, load_json_data

logging = logging.getLogger(__name__)


class SheriffSale:
    """
    Web scraper for sheriff sale website
    """

    def __init__(self, county=None):

        self.county_name = county
        self.county_id = self.county_name and self.get_sheriff_sale_county_id(
            self.county_name
        )
        self.soup = None

        if county != None:
            try:
                sheriff_sale_county_url = (
                    "https://salesweb.civilview.com/Sales/SalesSearch?countyId="
                    + self.county_id
                )

                self.session = requests.Session()
                self.soup = requests_content(sheriff_sale_county_url, self.session)
            except ConnectionError as err:
                raise ConnectionError("Cannot Access URL: ", err)

            self.table_div = self.soup.find("table", class_="table table-striped")

            if not self.table_div:
                logging.error("The Sheriff Sale Table Div was not captured")

                return

    def get_sheriff_sale_county_id(self, county):
        nj_json_data = load_json_data("data/NJ_Data.json")
        sheriff_sale_county_id = nj_json_data[county]["sheriffSaleId"]

        return sheriff_sale_county_id

    def get_counties(self):
        """
        Gathers all counties that are listed on the sheriff sale website
        """
        sheriff_sales_url = "https://salesweb.civilview.com/"
        request = requests_content(sheriff_sales_url)

        trs = [x.text.strip().split() for x in request.find_all("tr")]
        counties = [tr[0] for tr in trs if tr[-1] == "NJ"]

        return counties

    def get_sale_dates(self):
        """
        Gathers all of sale dates available in the drop-down form
        """
        sale_dates = []
        selects = self.soup.find_all(name="select", attrs={"id": "PropertyStatusDate"})
        for select in selects:
            sale_dates = [
                option["value"] for option in select.find_all(name="option")[1:]
            ]

        return sale_dates

    def get_listings_details_links(self):
        """
        Gathers all of the href links for each listing and builds a list of all the links to each listing's details
        in the form of "https://salesweb.civilview.com/Sales/SaleDetails?PropertyId=563667001"
        """
        sale_links = []
        for row in self.soup.find_all("td", attrs={"class": "hidden-print"}):
            for link in row.find_all("a", href=True):
                sale_links.append("https://salesweb.civilview.com" + link["href"])

        return sale_links

    def get_property_ids(self):
        """
        Gathers all the property id's from all of the href links for each listing under details
        E.g. '563663246' from "/Sales/SaleDetails?PropertyId=563663246"
        """
        sale_links = self.get_listings_details_links()
        property_ids = [re.findall(r"\d{9}", x)[0] for x in sale_links]

        return property_ids

    def get_sheriff_ids(self):
        """
        Gathers all the sheriff id's from the table_data
        'F-18001491'
        """

        sheriff_ids = []
        for row in self.table_div.find_all("tr")[1:]:
            sheriff_ids.append(row.find_all("td")[1].text)

        return sheriff_ids

    def get_address_data(self):
        """
        Gathers all of the address data for each listing
        """

        address_data = []
        for tr in self.soup.find_all("tr")[1:]:
            for td in tr.find_all("td")[5::5]:
                address_data.append(td.text)

        return address_data

    def get_all_listing_details_tables(self):
        """
        Retrieves all table html data from each listings details.
        """
        sale_links = self.get_listings_details_links()

        listings_table_data = []

        for links in sale_links:
            request = requests_content(links, self.session)
            html = request.find("div", class_="table-responsive")

            listings_table_data.append(html)

        return listings_table_data
