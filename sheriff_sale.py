from bs4 import BeautifulSoup
from selenium import webdriver
from constants import *
from datetime import datetime
import pandas as pd
import requests
import json
import re
import os


class SheriffSale:
    def __init__(self):
        try:
            self.data = requests.get(sheriff_sales_url)
        except ConnectionError:
            print("Cannot Access URL")

        self.table_addr = []
        self.addresses = []
        self.cities = []
        self.zip_codes = []

        self.run_selenium()

    def run_selenium(self):
        sale_dates = []
        table_data = []
        today_date = datetime.now().date()

        if not os.path.exists('{}.html'.format(today_date)):
            driver = webdriver.Chrome()
            driver.get(sheriff_sales_url)
            driver.maximize_window()

            date = driver.find_elements_by_xpath('//select[@id="PropertyStatusDate"]/option')
            for dates in date:
                sale_dates.append(dates.get_attribute('value'))

            sale_dates.pop(0)
            driver.find_element_by_xpath('//select[@id="PropertyStatusDate"]/option[@value="{}"]'.format(sale_dates[1])).click()
            driver.find_element_by_css_selector("[type=submit]").click()

            print("--HTML has been gathered--")

            page_source = driver.page_source
            _html = BeautifulSoup(page_source, 'html.parser')

            print("Appending all addresses from Sheriff Sale Website...\n")

            for row in _html.find_all('tr'):
                table_data.append([td.text for td in row.find_all('td')])

            for i in table_data[1:]:
                self.table_addr.append(i[5])
            driver.close()

    def cleanup(self):
        for key, value in replace_dict.items():
            self.table_addr = [re.sub(r'\b({})\b'.format(key), value, x) for x in self.table_addr]

        text = []
        regex = re.compile(r'|'.join(city_list))

        for addr in self.table_addr:
            a = re.split(regex, addr)
            text.append(a[0])

        for i in text:
            print(i)

    def city_match(self):
        json_string = open('zip_cities.json', 'r').read()
        json_object = json.loads(json_string)

        for i in self.zip_codes:

            if i in json_object.keys():
                self.cities.append(json_object[i])

            elif i not in json_object.keys():
                self.cities.append('*missing*')


if __name__ == "__main__":
    main = SheriffSale()

    main.city_match()
    main.cleanup()

    print('\n')
    print('Results:')
    print('Total of {} elements in [table_addr]'.format(len(main.table_addr)))
    print('Total of {} elements in [addresses]'.format(len(main.addresses)))
    print('Total of {} elements in [cities]'.format(len(main.cities)))
    print('Total of {} elements in [zip_codes]'.format(len(main.zip_codes)))
