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
        driver = webdriver.Chrome()
        driver.get(sheriff_sales_url)
        driver.maximize_window()

        # Find date drop down, grab the text
        date = driver.find_elements_by_xpath('//select[@id="PropertyStatusDate"]/option')
        sales_date = [dates.get_attribute('value') for dates in date]
        sales_date.pop(0)   # Remove initial blank date
        sales_date_xpath = '//select[@id="PropertyStatusDate"]/option[@value="{}"]'
        driver.find_element_by_xpath(sales_date_xpath.format(sales_date[0])).click()
        driver.find_element_by_css_selector("[type=submit]").click()

        page_source = driver.page_source
        html = BeautifulSoup(page_source, 'html.parser')

        # html_tr = [row for row in html.find_all('tr')]

        table_data = []
        for row in html.find_all('tr'):
            table_data.append([td.text for td in row.find_all('td')])

        driver.close()

        # Cleanup
        table_addr = [data[5] for data in table_data[1:]]
        for key, value in replace_dict.items():
            table_addr = [re.sub(r'\b({})\b'.format(key), value, x) for x in table_addr]

        # Search
        regex_street_suffix = re.compile(r'(.*(?:' + r'|'.join(street_suffix) + r'))+\s(.*)+')
        regex_city = re.compile(r'|'.join(city_list))
        regex_zip_code = re.compile(r'\d{5}')

        street_match = [regex_street_suffix.findall(row)[0][0] for row in table_addr]
        city_match = [regex_city.findall(row)[0] for row in table_addr]
        zip_match = [regex_zip_code.findall(row)[0] for row in table_addr]

        result = list(zip(street_match, city_match, zip_match))
        for i in result:
            print(i)

if __name__ == "__main__":
    main = SheriffSale()
