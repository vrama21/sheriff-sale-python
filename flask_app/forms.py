from flask_app import sheriff_sale
import itertools
from flask_app import load_json_data
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

data = load_json_data("NJParcels_CityNums.json")
counties = sorted(list(data.keys()))

cities = [data[x].keys() for x in counties]
cities = sorted(itertools.chain.from_iterable(cities))

_COUNTIES = [(x, x) for x in counties]
_CITIES = [(x, x) for x in cities]
_SALE_DATES = [(x, x) for x in sheriff_sale.get_sale_dates()]

_COUNTIES.insert(0, ("", "-All-"))
_CITIES.insert(0, ("", "-All-"))
_SALE_DATES.insert(0, ("", "-All-"))


class SearchFilter(FlaskForm):
    county = SelectField("Select a County", choices=_COUNTIES)
    city = SelectField("Select a City", choices=_CITIES)
    sale_date = SelectField(
        label="Select a Date", choices=_SALE_DATES, id="sale-date-select-field"
    )

