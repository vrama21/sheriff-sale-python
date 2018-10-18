from bs4 import BeautifulSoup
from constants import SHERIFF_SALES_URL, SHERIFF_SALES_BASE_URL, SUFFIX_ABBREVATIONS, ADDRESS_REGEX_SPLIT, CITY_LIST
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

    def get_sale_dates(self):
        sale_dates = []
        soup = requests_content(SHERIFF_SALES_URL, self.session)
        for select in soup.find_all(name='select', attrs={'id': 'PropertyStatusDate'}):
            sale_dates = [option['value'] for option in select.find_all(name='option')[1:]]
        return sale_dates

    def sheriff_sale_dict(self, table_data):
        table_dict = {
            'sheriff#': [x[0] for x in table_data],
            'court_case#': [x[1] for x in table_data],
            'sale_date': [x[2] for x in table_data],
            'plaintiff': [x[3] for x in table_data],
            'defendant': [x[4] for x in table_data],
            'address': [x[5] for x in table_data],
            'priors': [x[6] for x in table_data],
            'attorney': [x[7] for x in table_data],
            'judgment': [x[8] for x in table_data],
            'deed': [x[9] for x in table_data],
            'deed_address': [x[10] for x in table_data],
        }

        return table_dict

    def sanitized_dict(self, sanitized_table):
        sanitized_dict = {
            'address': [x[0] for x in sanitized_table],
            'unit': [x[1] for x in sanitized_table],
            'city': [x[2] for x in sanitized_table],
            'zip_code': [x[3] for x in sanitized_table],
        }

        return sanitized_dict

    def sheriff_sale_sanitized(self, table_data):
        """
        Returns lists of sanitized address data in the format of (Address, Unit, City, Zip Code)
        """
        regex_street = re.compile(r'.*?(?:' + r'|'.join(ADDRESS_REGEX_SPLIT) + r')')
        regex_unit = re.compile(r'(Unit\s[0-9A-Za-z-]+)')
        regex_city = re.compile(r'|'.join(CITY_LIST))
        regex_zip_code = re.compile(r'\d{5}')

        # TODO: Figure out a way to print out which element in the list gives an attribute error.
        # Use only for testing nonetype data that needs to be adjusted in the constants
        # street_match = [regex_street.findall(row) for row in table_dict['address']]
        # city_match = [regex_city.findall(row) for row in table_data['address']]

        street_match = [re.search(regex_street, row).group(0).rstrip() for row in (table_data['address'])]
        for key, value in SUFFIX_ABBREVATIONS.items():
            street_match = [re.sub(fr'({key})', value, row) for row in street_match]

        # TODO: May run into a problem where city names are located in the streeg (e.g. 123 Mays Landing Rd)
        city_match = [re.search(regex_city, row).group(0) for row in table_data['address']]
        zip_match = [re.search(regex_zip_code, row).group(0) for row in table_data['address']]
        unit_match = [regex_unit.findall(row) for row in table_data['address']]

        for i, unit in enumerate(unit_match):
            if unit:
                unit_match[i] = unit[0]
            else:
                unit_match[i] = ''

        # TODO: Do I need this when I can just access all the data from the dictionary??
        result = list(zip(street_match, unit_match, city_match, zip_match))

        return result

    def selenium_driver(self, sale_date):
        """
        Runs the selenium driver to gather all table data on the sheriff sale website
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

        sale_details_table = []
        for row in soup.find_all('tr')[1:]:
            for link in row.find_all('a', href=True):
                sale_details_table.append(link['href'])

        sale_details_links = []
        for i, links in enumerate(sale_details_table):
            sale_details_links.append(SHERIFF_SALES_BASE_URL + sale_details_table[i])

        listings_table_data = []
        status_history_data = []
        for links in sale_details_links:
            listing_html = (requests_content(links, self.session))
            listings_table_data.append(listing_html.find('table', {'class': 'table table-striped'}))
            status_history_data.append(listing_html.find('table', {'class': 'table table-striped '}))

        listing_details = []
        maps_href_link = []
        for table_data in listings_table_data:
            listing_details.append([x.text for x in table_data.find_all('td')[1::2]])
            for link in table_data.find_all('a', href=True):
                maps_href_link.append(link['href'])

        status_history = []
        for table_data in status_history_data:
            status_history.append([x.text for x in table_data.find_all('td')])

        # print(listing_details, maps_href_link, status_history)
        return listing_details, maps_href_link, status_history


if __name__ == "__main__":
    sheriff = SheriffSale()
    sale_date = sheriff.get_sale_dates()
    listing_details = sheriff.selenium_driver(sale_date[0])
    print(listing_details, '\n')
    print(listing_details[0])
    # sheriff_dict = sheriff.sheriff_sale_dict(listing_details)
    # print('Not Santitized Address Data:', '\n', sheriff_dict['address'], '\n')
    #
    # sanitized = sheriff.sheriff_sale_sanitized(sheriff_dict)
    # print('Sanitized Address Data:', '\n', sanitized)
    #
    # sanitized_dict = sheriff.sanitized_dict(sanitized)
    # print(sanitized_dict['city'])

