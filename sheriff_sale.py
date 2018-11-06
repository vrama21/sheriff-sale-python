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

    def get_sale_dates(self):
        """
        Opens sheriff sale website and grabs all sale dates available in the drop-down form
        """

        sale_dates = []
        soup = requests_content(SHERIFF_SALES_URL, self.session)
        for select in soup.find_all(name='select', attrs={'id': 'PropertyStatusDate'}):
            sale_dates = [option['value'] for option in select.find_all(name='option')[1:]]
        return sale_dates

    def sheriff_sale_dict(self, complete_data):
        """
        Place all gathered data from sheriff sale in an organized dictionary
        """
        list_dicts = []
        for data in complete_data:
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
                     'maps_href': data[3],
                     'status_history': data[4]
                     }
            list_dicts.append(_dict)

        return list_dicts

        # _dict = {'property_id': [x[0] for x in complete_data],
            #          'listing_details': {
            #             'sheriff': [x[1][0] for x in complete_data],
            #             'court_case': [x[1][1] for x in complete_data],
            #             'sale_date': [datetime.strptime(x[1][2], '%m/%d/%Y').strftime('%m/%d/%Y') for x in complete_data],
            #             'plaintiff': [x[1][3] for x in complete_data],
            #             'defendant': [x[1][4] for x in complete_data],
            #             'address': [x[1][5] for x in complete_data],
            #             'priors': [x[1][6] for x in complete_data],
            #             'attorney': [x[1][7] for x in complete_data],
            #             'judgment': [x[1][8] for x in complete_data],
            #             'deed': [x[1][9] for x in complete_data],
            #             'deed_address': [x[1][10] for x in complete_data],
            #          },
            #          'sanitized': {
            #             'address': [x[2][0] for x in complete_data],
            #             'unit': [x[2][1] for x in complete_data],
            #             'city': [x[2][2] for x in complete_data],
            #             'zip_code': [x[2][3] for x in complete_data]
            #          },
            #          'maps_href': [x[3] for x in complete_data],
            #          'status_history': [x[4] for x in complete_data]
            #          }
            #
            # return _dict

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

    def build_dict(self):
        soup = requests_content(SHERIFF_SALES_URL, self.session)

        sales_href = []
        for row in soup.find_all('tr')[1:]:
            for link in row.find_all('a', href=True):
                sales_href.append(link['href'])

        sales_links = []
        for i, links in enumerate(sales_href):
            sales_links.append(SHERIFF_SALES_BASE_URL + sales_href[i])

        property_id = [re.findall('\d{9}', x)[0] for x in sales_href]

        listings_table_data = []
        status_history_data = []
        for links in sales_links:
            listing_html = requests_content(links, self.session)
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

        sanitized_listing_details = self.sanitize_address_data(listing_details)

        zipped = list(zip(property_id, [x for x in listing_details], sanitized_listing_details,
                      maps_href_link, status_history))

        zip_dict = self.sheriff_sale_dict(zipped)

        return zip_dict


if __name__ == "__main__":
    sheriff = SheriffSale()
    # sale_date = sheriff.get_sale_dates()
    complete_data = sheriff.build_dict()
    print(complete_data)
    import json
    with open('sheriff_sale_dump.json', 'w') as f:
        json.dump(complete_data, f)
