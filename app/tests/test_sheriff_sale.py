# from .constants import ADDRESS_REGEX_SPLIT, CITY_LIST
# import re
# from sheriff_sale import SheriffSale
# import unittests


# class TestSheriffSale:
#     def __init__(self):
#         self.sheriff_sale = SheriffSale()

#     def test_sanitize_address_data(self):
#         table_data = self.sheriff_sale.get_table_data()

#         regex_street = re.compile(r'.*?(?:' + r'|'.join(ADDRESS_REGEX_SPLIT) + r')')
#         regex_city = re.compile(r'(' + '|'.join(CITY_LIST) + ') NJ')

#         address_data = [x[0][5] for x in table_data]
#         print(address_data)

#         street_match = [regex_street.findall(row) for row in address_data]
#         city_match = [regex_city.findall(row) for row in address_data]

#         print(street_match)


# if __name__ == '__main__':
#     test = TestSheriffSale()
#     test.test_sanitize_address_data()
