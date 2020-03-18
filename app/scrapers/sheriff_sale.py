import json
import logging
import re
import requests
from datetime import datetime, date
from pathlib import Path
from urllib.parse import quote
from utils import requests_content, load_json_data
from constants import (
    SHERIFF_SALES_URL,
    SHERIFF_SALES_BASE_URL,
    SHERIFF_SALE_JSON_DATA,
    SUFFIX_ABBREVATIONS,
    ADDRESS_REGEX_SPLIT,
    CITY_LIST,
)

logging.basicConfig(
    filename="logs/sheriff_sale.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


class SheriffSale:
    """
    Web scraper for sheriff sale website
    """

    def __init__(self, county_id):

        try:
            self.data = requests.get(SHERIFF_SALES_URL)
        except ConnectionError as err:
            raise ConnectionError("Cannot Access URL: ", err)

        self.county_id = county_id
        self.session = requests.Session()

        self.soup = requests_content(
            f"{SHERIFF_SALES_URL}{self.county_id}", self.session
        )
        self.table_div = self.soup.find("div", class_="table-responsive")

    def get_sale_dates(self):
        """
        Gathers all of sale dates available in the drop-down form
        """
        sale_dates = []
        for select in self.soup.find_all(
            name="select", attrs={"id": "PropertyStatusDate"}
        ):
            sale_dates = [
                option["value"] for option in select.find_all(name="option")[1:]
            ]

        sale_dates = [x.replace("/", "-") for x in sale_dates]

        return sale_dates

    def get_sale_links(self):
        """
        Gathers all of the href links for each listing and builds a list of all the links to each listing's details
        in the form of "https://salesweb.civilview.com/Sales/SaleDetails?PropertyId=563667001"
        """
        sale_links = []
        for row in self.soup.find_all("td", attrs={"class": "hidden-print"}):
            for link in row.find_all("a", href=True):
                sale_links.append(SHERIFF_SALES_BASE_URL + link["href"])

        return sale_links

    def get_property_ids(self):
        """
        Gathers all the property id's from all of the href links for each listing under details
        E.g. '563663246' from "/Sales/SaleDetails?PropertyId=563663246"
        """
        sale_links = self.get_sale_links()
        property_id = [re.findall(r"\d{9}", x)[0] for x in sale_links]

        return property_id

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
        """Gathers all of the address data for each listing"""

        address_data = []
        for row in self.soup.find_all("tr")[1:]:
            for td in row.find_all("td")[5::5]:
                address_data.append(td.text)

        return address_data

    def get_all_listing_details_tables(self):
        """
        Retrieves all table html data from each listings details. Run this once since its running 
        several requests on hundreds of links.
        """
        sale_links = self.get_sale_links()
        listings_table_data = []
        for links in sale_links:
            html = requests_content(links, self.session)
            listings_table_data.append(html.find("div", class_="table-responsive"))

        return listings_table_data

    def get_table_data(self):
        """
        Retrives data from each listing's detail page. Returns a list of table data,
        a google maps url, the status history.
        """
        listing_details_tables = self.get_all_listing_details_tables()

        table_data_html, status_history_html = [], []
        table_data, maps_url, status_history = [], [], []

        # Grabs all of the html for table data and status history
        for listing in listing_details_tables:
            table_data_html.append(listing.find("table", class_="table table-striped"))
            status_history_html.append(
                listing.find("table", class_="table table-striped ")
            )

        # Parses html to grab the table data as well as the google maps url
        for table in table_data_html:
            table_data.append([x.text for x in table.find_all("td")[1::2]])
            for link in table.find_all("a", href=True):
                maps_url.append(link["href"])

        # Converts the sale_date data from '1/1/2019' to '1-1-2019'
        regex_sale_date = re.compile(r"(?![0-9]+)(\/)")
        for listing in table_data:
            listing[2] = re.sub(regex_sale_date, "-", listing[2])

        # Grabs the status history for each address
        for status in status_history_html:
            try:
                status_history.append([x.text for x in status.find_all("td")])
            except AttributeError:
                status_history.append([])

        table_dict = {
            "table_data": table_data,
            "maps_url": maps_url,
            "status_history": status_history,
        }

        return table_dict

    def sanitize_address_data(self):
        """
        Returns lists of sanitized address data in the format of (Address, Unit, City, Zip Code)
        """
        regex_street = re.compile(r".*?(?:" + r"|".join(ADDRESS_REGEX_SPLIT) + r")\s")
        regex_city = re.compile(r"(" + "|".join(CITY_LIST) + ") NJ")
        regex_unit = re.compile(r"(Unit|Apt).([0-9A-Za-z-]+)")
        regex_secondary_unit = re.compile(r"(Building|Estate) #?([0-9a-zA-Z]+)")
        regex_zip_code = re.compile(r"\d{5}")

        address_data = self.get_address_data()

        street_match, city_match = [], []

        for row in address_data:
            try:
                street_match.append(re.search(regex_street, row).group(0).rstrip())
                city_match.append(re.search(regex_city, row).group(1))

            except AttributeError as e:
                logging.info(e)
                logging.error(row)

        print("Street Match: " + str(street_match))
        print("City Match: " + str(city_match))

        unit_match = self.match_parser(address_data, regex_unit)
        secondary_unit_match = self.match_parser(address_data, regex_secondary_unit)
        zip_match = self.match_parser(address_data, regex_zip_code)

        # TODO: Do it only on the last word to avoid instances such as (1614 W Ave)
        # Abbreviates all street suffixes (e.g. Street, Avenue to St and Ave)
        for key, value in SUFFIX_ABBREVATIONS.items():
            street_match = [re.sub(fr"({key})", value, row) for row in street_match]

        result = list(
            zip(street_match, unit_match, secondary_unit_match, city_match, zip_match)
        )

        return result

    def match_parser(self, address_data, regex):
        match_results = []
        for row in address_data:
            match = re.search(regex, row)
            if match is None:
                match_results.append("")
            else:
                match_results.append(match.group(0))
        return match_results

    def main(self):
        """
        Structures all sheriff sale data in a list of dictionaries
        """

        property_id = self.get_property_ids()
        table_data = self.get_table_data()
        sanitized_table_data = self.sanitize_address_data()

        zipped = list(
            zip(
                property_id,
                [x for x in table_data["table_data"]],
                sanitized_table_data,
                table_data["maps_url"],
                table_data["status_history"],
            )
        )

        data_list = []
        for d in zipped:
            data = {
                "property_id": d[0],
                "listing_details": {
                    "sheriff": d[1][0],
                    "court_case": d[1][1],
                    # "sale_date": datetime.strptime(d[1][2], "%m-%d-%Y").strftime(
                    #     "%m-%d-%Y"
                    # ),
                    "plaintiff": d[1][3],
                    "defendant": d[1][4],
                    "address": d[1][5],
                    "priors": d[1][6],
                    "attorney": d[1][7],
                    "judgment": d[1][8],
                    "deed": d[1][9],
                    "deed_address": d[1][10],
                },
                "sanitized": {
                    "address": d[2][0],
                    "unit": d[2][1],
                    "secondary_unit": d[2][2],
                    "city": d[2][3],
                    "zip_code": d[2][4],
                },
                "maps_url": d[3],
                "status_history": d[4],
            }
            data_list.append(data)

        return data_list


if __name__ == "__main__":
    SHERIFF = SheriffSale("25")
    main = SHERIFF.main()
