from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import requests
import json
import re


class Main:
    sheriff_sales_url = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=25'
    nj_parcels_url = 'http://njparcels.com/property/'
    nj_parcels_api_url = 'http://njparcels.com/api/v1.0/property/'
    trulia_url = 'https://www.trulia.com/'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    # From http://www.whoishostingthis.com/tools/user-agent/

    sale_date = "'02/22/2018'"
    data = requests.get(sheriff_sales_url)
    html = data.text
    sheriff_sale_html = BeautifulSoup(html, 'html.parser')

    def __init__(self):
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

        driver.find_element_by_xpath("//select[@id='PropertyStatusDate']/option[@value=" + self.sale_date + "]").click()
        driver.find_element_by_css_selector("[type=submit]").click()

        print("--HTML has been gathered--")
        page_source = driver.page_source

        html = BeautifulSoup(page_source, 'html.parser')

        print("Appending all addresses from Sheriff Sale Website...\n")

        for row in html.find_all('tr'):
            self.table_data.append([td.text for td in row.find_all('td')])

        for i in self.table_data[1:]:
            self.table_addr.append(i[5])

        self.address_clean_up()

        print('Total of {} elements in [table.addr]'.format(len(self.table_addr)))
        print(self.table_addr)

        self.data_frame()

        driver.close()

    def data_frame(self):
        # TODO: Clean up the regex expression
        # Partially Works
        # add_pattern = re.compile(r'\d{1,5}\s\w+\s\w+\s\w+\s\w+\s\w+\s\w+', re.MULTILINE)

        # Test a new regex

        add_pattern = re.compile(r'\d{1,5}\s\w+\s\w+\s\w+', re.MULTILINE)
        add_match = add_pattern.findall(str(self.table_addr))

        # city_pattern = re.compile(r' ')
        # city_match = city_pattern.findall(str(self.table_addr))

        zip_pattern = re.compile(r'(0\d{4})+')
        zip_match = zip_pattern.findall(str(self.table_addr))

        for match in add_match:
            self.addresses.append(match)

        self.city_match()

        self.zip_match()

        for match in zip_match:
            self.zip_codes.append(match)

        self.address_clean_up()
        # self.address_split()

        print("\n--All addresses have been pulled from the Sheriff Sale Website--")
        print("A total of {} addresses are listed".format(str(len(self.addresses))))
        print("A total of {} cities are listed".format(str(len(self.cities))))
        print("A total of {} zip codes are listed".format(str(len(self.zip_codes))))

        # self.nj_parcels_driver()

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

        # pattern = re.findall(r'NJ', self.table_addr)
        # self.table_addr = [x.sub(' NJ', '') for x in self.table_addr)]

    def cities_list(self):
        with open('cities.txt', 'r') as f:
            city = [line.strip() for line in f]
        return city

    def city_match(self):
        city_list = self.cities_list()
        string = self.table_addr
        _cities = re.findall(r'\b(?:%s)\b' % '|'.join(city_list), str(string))
        print('Total number of listed address {}'.format(len(_cities), '\n'))
        self.cities.append(_cities)

    def zip_match(self):
        string = self.table_addr
        zips = re.findall(r'\d{5}', str(string))
        print('Total of {} elements in [zip_codes]'.format(len(self.table_addr)))
        print(zips)

    def address_split(self):
        pass
        # df5_rows = self.df5.rows()
        # add_pattern = re.finditer(r'\d{1,5}\s\w+\s\w+\s\w+')
        # add_match = add_pattern.findall(df5)
        # print(df5_rows)

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
