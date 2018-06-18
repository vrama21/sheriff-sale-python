from bs4 import BeautifulSoup
from selenium import webdriver
from constants import *
import requests
import re


class SheriffSale:
    def __init__(self):
        try:
            self.data = requests.get(sheriff_sales_url)
        except ConnectionError:
            print("Cannot Access URL")

        self.address_data = []

        self.run_selenium()

    def __repr__(self):
        self.__repr__ = self.__str__
        return

    def __str__(self):
        return str(self.address_data)

    def run_selenium(self):
        sale_dates = []
        table_data = []
        table_addr = []

        driver = webdriver.Chrome()
        driver.get(sheriff_sales_url)
        driver.maximize_window()

        date = driver.find_elements_by_xpath('//select[@id="PropertyStatusDate"]/option')
        for dates in date:
            sale_dates.append(dates.get_attribute('value'))

        sale_dates.pop(0)
        driver.find_element_by_xpath('//select[@id="PropertyStatusDate"]/option[@value="{}"]'.format(sale_dates[1])).click()
        driver.find_element_by_css_selector("[type=submit]").click()

        page_source = driver.page_source
        _html = BeautifulSoup(page_source, 'html.parser')

        for row in _html.find_all('tr'):
            table_data.append([td.text for td in row.find_all('td')])

        for i in table_data[1:]:
            table_addr.append(i[5])
        driver.close()

        # Cleanup
        for key, value in replace_dict.items():
            table_addr = [re.sub(r'\b({})\b'.format(key), value, x) for x in table_addr]

        regex_by_city = re.compile(r'|'.join(city_list))
        # regex_by_street_suffix = re.compile(r'\b|\b'.join(street_suffix))
        regex_by_street_suffix = re.compile(r"(.+)\s*(" + r'\b|\b'.join(street_suffix) + r")\s*(.+)")
        print(regex_by_street_suffix)

        # a = [re.split(regex_by_street_suffix, row) for row in table_addr]
        a = [re.search(regex_by_street_suffix, row).groups() for row in table_addr]
        address = [''.join(x[0:2]) for x in a]
        for i in address:
            print(i)



        # for row in table_addr:
        #     initial_split = row.split('NJ')
        #     address_0 = initial_split[0]
        #     zip_code = initial_split[-1]
        #
        #     address = re.split(regex_by_city, str(address_0))
        #     address = [x.split(' (') for x in address]
        #     # a2 = [x.split(' )') for x in a1[1]]
        #
        #     # print(initial_split)
        #     print(address[0][0])
        #     print(zip_code)
        # # return self.address_data


if __name__ == "__main__":
    main = SheriffSale()
    print(main)
