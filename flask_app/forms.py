from flask_app import sheriff_sale, load_json_data, CITY_LIST, COUNTY_LIST
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

COUNTIES = [(x, x) for x in COUNTY_LIST]
CITIES = [(x, x) for x in CITY_LIST]
SALE_DATES = [(x, x) for x in sheriff_sale.get_sale_dates()]

COUNTIES.insert(0, ("", "-All-"))
CITIES.insert(0, ("", "-All-"))
SALE_DATES.insert(0, ("", "-All-"))


class SearchFilter(FlaskForm):
    county = SelectField("Select a County", choices=COUNTIES)
    city = SelectField("Select a City", choices=CITIES)
    sale_date = SelectField(
        label="Select a Date", choices=SALE_DATES, id="sale-date-select-field"
    )

