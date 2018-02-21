"""
TODO: - Split [self.table.addr] for clean address data
TODO: - Refactor address_clean_up?
TODO: - Figure out x.replace("North") to not affect Northfield
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import requests
import json
import re


class Main:
    nj_parcels_url = 'http://njparcels.com/property/'
    nj_parcels_api_url = 'http://njparcels.com/api/v1.0/property/'
    trulia_url = 'https://www.trulia.com/'
    # header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    # From http://www.whoishostingthis.com/tools/user-agent/

    def __init__(self):
        self.sheriff_sales_url = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=25'

        try:
            self.data = requests.get(self.sheriff_sales_url)
        except ConnectionError:
            print("Cannot Access URL")

        self.sale_dates = []
        self.table_data = []
        self.table_addr = []
        self.addresses = []
        self.cities = []
        self.zip_codes = []

        self.main()

    def main(self):
        driver = webdriver.Chrome()
        driver.get(self.sheriff_sales_url)
        driver.maximize_window()

        date = driver.find_elements_by_xpath('//select[@id="PropertyStatusDate"]/option')
        for dates in date:
            self.sale_dates.append(dates.get_attribute('value'))

        self.sale_dates.pop(0)
        # self.sale_dates = [(', '.join('"' + item + '"' for item in self.sale_dates))]

        driver.find_element_by_xpath('//select[@id="PropertyStatusDate"]/option[@value="' + self.sale_dates[0] + '"]').click()
        driver.find_element_by_css_selector("[type=submit]").click()

        print("--HTML has been gathered--")
        page_source = driver.page_source

        _html = BeautifulSoup(page_source, 'html.parser')

        print("Appending all addresses from Sheriff Sale Website...\n")

        for row in _html.find_all('tr'):
            self.table_data.append([td.text for td in row.find_all('td')])

        for i in self.table_data[1:]:
            self.table_addr.append(i[5])

        self.address_match()
        self.zip_match()
        self.city_match()
        self.address_split()
        self.address_clean_up()
        self.data_frame()

        print('\n')
        print('Results:')
        print('Total of {} elements in [table_addr]'.format(len(self.table_addr)))
        print('Total of {} elements in [addresses]'.format(len(self.addresses)))
        print('Total of {} elements in [cities]'.format(len(self.cities)))
        print('Total of {} elements in [zip_codes]'.format(len(self.zip_codes)))

        driver.close()

    def data_frame(self):
        df = pd.DataFrame({'Address': self.table_addr,
                           'City': self.cities,
                           'Zip Code': self.zip_codes})
        pd.set_option('display.max_rows', 1000)
        pd.set_option('max_colwidth', 60)
        print(df['Address'])

    def address_clean_up(self):
        self.table_addr = [x.replace('Avenue', 'Ave') for x in self.table_addr]
        self.table_addr = [x.replace('Drive', 'Dr') for x in self.table_addr]
        self.table_addr = [x.replace('Street', 'St') for x in self.table_addr]
        self.table_addr = [x.replace('Road', 'Rd') for x in self.table_addr]
        self.table_addr = [x.replace('Boulevard', 'Blvd') for x in self.table_addr]
        self.table_addr = [x.replace('Court', 'Ct') for x in self.table_addr]
        self.table_addr = [x.replace('Circle', 'Cir') for x in self.table_addr]
        self.table_addr = [x.replace('Lane', 'Ln') for x in self.table_addr]

        self.table_addr = [x.replace('North', 'N') for x in self.table_addr]
        self.table_addr = [x.replace('South', 'S') for x in self.table_addr]
        self.table_addr = [x.replace('East', 'E') for x in self.table_addr]
        self.table_addr = [x.replace('West', 'W') for x in self.table_addr]

    def cities_list(self):
        with open('cities.txt', 'r') as f:
            city = [line.strip() for line in f]
        return city

    def address_match(self):
        # for i in self.table_addr:

        # json_data = open('zip_codes.json', 'r').read()
        # data = json.loads(json_data)
        # print(data)
        pass

    def city_match(self):
        json_string = open('zip_cities.json', 'r').read()
        json_object = json.loads(json_string)
        for i in self.zip_codes:
            if i in json_object.keys():
                self.cities.append(json_object[i])
            elif i not in json_object.keys():
                self.cities.append('*missing*')

    def zip_match(self):
        _zip_pattern = re.compile(r'\d{5}')
        _zip_match = _zip_pattern.findall(str(self.table_addr))
        for match in _zip_match:
            self.zip_codes.append(match)

    def address_split(self):
        # _add_pattern = re.compile(r'\b(?:%s)\b' % '|'.split('NJ'))
        _city_list = self.cities_list()
        _add_pattern = re.compile(r'(\b(?<=%s)\b' % '|'.join(_city_list))
        _add_match = _add_pattern.findall(str(self.table_addr))
        for match in _add_match:
            self.addresses.append(match)
        print(self.addresses)

    def nj_parcels_driver(self):
        driver = webdriver.Chrome()
        driver.get(self.nj_parcels_url)
        driver.maximize_window()

        driver.find_element_by_xpath("//select[@name='s_co']/option[@value='01']").click()

        for address in self.addresses:
            text_box = driver.find_element_by_css_selector('#s_addr')
            text_box.send_keys(address)
            driver.find_element_by_css_selector('#btn_addr').click()

            driver.find_element_by_link_text(self.addresses[0]).click()
            driver.find_element_by_css_selector("a[href$='.json']").click()


if __name__ == "__main__":
    Main()
