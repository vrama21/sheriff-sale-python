from flask_app import sheriff_sale
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

SHERIFF_SALE_DATES = [(x.replace('/', '-'), x) for x in sheriff_sale.get_sale_dates()]


class SaleDateForm(FlaskForm):
    sale_date = SelectField(label='Select a Date', choices=SHERIFF_SALE_DATES)
    submit = SubmitField(label='Submit')