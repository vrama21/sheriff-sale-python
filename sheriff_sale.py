from bs4 import BeautifulSoup
from constants import SHERIFF_SALES_URL, SHERIFF_SALES_BASE_URL, SUFFIX_ABBREVATIONS, ADDRESS_REGEX_SPLIT, CITY_LIST
from datetime import datetime
from selenium import webdriver
from utils import requests_content
import requests
import re


class SheriffSale:
    """
    Web scraper for sheriff sale website
    """
    def __init__(self):

        try:
            self.data = requests.get(SHERIFF_SALES_URL)
        except ConnectionError as err:
            raise ConnectionError("Cannot Access URL: ", err)

        self.session = requests.Session()
        self.soup = requests_content(SHERIFF_SALES_URL, self.session)

    def get_sale_dates(self):
        """
        Gathers all of sale dates available in the drop-down form
        """

        sale_dates = []
        for select in self.soup.find_all(name='select', attrs={'id': 'PropertyStatusDate'}):
            sale_dates = [option['value'] for option in select.find_all(name='option')[1:]]

        return sale_dates

    def get_sale_links(self):
        """
        Gathers all of the href links for each listing and builds a list of all the links to each listing's details
        in the form of "https://salesweb.civilview.com/Sales/SaleDetails?PropertyId=563667001"
        """
        sale_links = []
        for row in self.soup.find_all('tr')[1:]:
            for link in row.find_all('a', href=True):
                sale_links.append(SHERIFF_SALES_BASE_URL + link['href'])

        return sale_links

    def get_property_ids(self):
        """
        Gathers all the property id's from all of thge href links for each listing under details
        E.g. '563663246' from "/Sales/SaleDetails?PropertyId=563663246"
        """
        sale_links = self.get_sale_links()
        property_id = [re.findall('\d{9}', x)[0] for x in sale_links]

        return property_id

    def get_all_listing_details_tables(self):
        """
        Retrieves all table html data from each listings details. Run this once since its running several
        requests on hundreds of links.
        """
        sale_links = self.get_sale_links()
        listings_table_data = []
        for links in sale_links:
            html = requests_content(links, self.session)
            listings_table_data.append(html.find('div', class_='table-responsive'))

        return listings_table_data

    def get_table_data(self):
        listing_details_tables = self.get_all_listing_details_tables()
        table_data_html, status_history_html = [], []
        table_data, maps_url, status_history = [], [], []
        for listing in listing_details_tables:
            table_data_html.append(listing.find('table', class_='table table-striped'))
            status_history_html.append(listing.find('table', class_='table table-striped '))

        for table in table_data_html:
            table_data.append([x.text for x in table.find_all('td')[1::2]])
            for link in table.find_all('a', href=True):
                maps_url.append(link['href'])

        for status in status_history_html:
            status_history.append([x.text for x in status.find_all('td')])

        return table_data, maps_url, status_history

    def sanitize_address_data(self, table_data):
        """
        Returns lists of sanitized address data in the format of (Address, Unit, City, Zip Code)
        """

        regex_street = re.compile(r'.*?(?:' + r'|'.join(ADDRESS_REGEX_SPLIT) + r')')
        regex_street2 = re.compile(r'.*?(?:Route\s\d+)')
        regex_unit = re.compile(r'(Unit\s[0-9A-Za-z-]+)')
        regex_city = re.compile(r'(' + '|'.join(CITY_LIST) + ') NJ')
        regex_zip_code = re.compile(r'\d{5}')

        address_data = [x[5] for x in table_data]

        # TODO: Figure out a way to print out which element in the list gives an attribute error.

        # TODO: Move these functions to testing
        # Use only for testing nonetype data that needs to be adjusted in the constants
        # street_find_all = [regex_street.findall(row) for row in address_data]
        # city_match = [regex_city.findall(row) for row in address_data]

        street_match = [re.search(regex_street, row).group(0).rstrip() for row in address_data]
        for key, value in SUFFIX_ABBREVATIONS.items():
            street_match = [re.sub(fr'({key})', value, row) for row in street_match]

        city_match = [re.search(regex_city, row).group(0) for row in address_data]
        zip_match = [re.search(regex_zip_code, row).group(0) for row in address_data]
        unit_match = [regex_unit.findall(row) for row in address_data]

        # TODO: May run into a problem where city names are located in the street (e.g. 123 Mays Landing Rd)

        for i, unit in enumerate(unit_match):
            if unit:
                unit_match[i] = unit[0]
            else:
                unit_match[i] = ''

        result = list(zip(street_match, unit_match, city_match, zip_match))

        return result

    # TODO: May deprecate since I'm gathering all data from site at once
    def selenium_driver(self, sale_date):
        """
        Runs the selenium driver to gather table data for a specified date
        on the sheriff sale website
        """
        driver = webdriver.Chrome()
        driver.get(SHERIFF_SALES_URL)
        driver.maximize_window()

        sales_date_xpath = f'//select[@id="PropertyStatusDate"]/option[@value="{sale_date}"]'
        driver.find_element_by_xpath(sales_date_xpath).click()
        driver.find_element_by_css_selector("[type=submit]").click()

        page_source = driver.page_source
        driver.close()

        soup = BeautifulSoup(page_source, 'html.parser')

        return soup

    def sheriff_sale_dict(self):
        """
        Structures all sheriff sale data in a list of dictionaries
        """

        property_id = self.get_property_ids()
        table_data = self.get_table_data()
        sanitized_table_data = self.sanitize_address_data(table_data[0])

        zipped = list(zip(property_id, [x for x in table_data[0]], sanitized_table_data,
                          table_data[1], table_data[2]))

        list_dicts = []
        for data in zipped:
            _dict = {'property_id': data[0],
                     'listing_details': {
                         'sheriff': data[1][0],
                         'court_case': data[1][1],
                         'sale_date': datetime.strptime(data[1][2], '%m/%d/%Y').strftime('%m/%d/%Y'),
                         'plaintiff': data[1][3],
                         'defendant': data[1][4],
                         'address': data[1][5],
                         'priors': data[1][6],
                         'attorney': data[1][7],
                         'judgment': data[1][8],
                         'deed': data[1][9],
                         'deed_address': data[1][10]
                     },
                     'sanitized': {
                         'address': data[2][0],
                         'unit': data[2][1],
                         'city': data[2][2],
                         'zip_code': data[2][3]
                     },
                     'maps_url': data[3],
                     'status_history': data[4]
                     }
            list_dicts.append(_dict)

        return list_dicts


if __name__ == "__main__":
    SHERIFF = SheriffSale()
    # sale_date = sheriff.get_sale_dates()
    DATA = SHERIFF.sheriff_sale_dict()
    print(DATA)
