from flask_app import sheriff_sale, COUNTIES, CITY_LIST
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

_COUNTIES = [(x, x) for x in COUNTIES]
_CITIES = [(x, x) for x in CITY_LIST]
_SALE_DATES = [(x, x) for x in sheriff_sale.get_sale_dates()]
_COUNTIES.insert(0, ("", "--All--"))
_CITIES.insert(0, ("", "--All--"))
_SALE_DATES.insert(0, ("", "--All--"))


class SearchFilter(FlaskForm):
    county = SelectField("Select a County", choices=_COUNTIES)
    city = SelectField("Select a City", choices=_CITIES)
    sale_date = SelectField(
        label="Select a Date", choices=_SALE_DATES, id="sale-date-select-field"
    )

