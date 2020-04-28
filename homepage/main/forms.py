from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, RadioField, DecimalField
from wtforms.validators import DataRequired, Length, Email
from flask import request


class ContactForm(FlaskForm):
    name = StringField('Name:', [
        DataRequired()])
    email = StringField('E-Mail:', [
        Email(message=('Not a valid email address.')),
        DataRequired()])
    body = TextAreaField('Message:', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


class BT_GeneralForm(FlaskForm):
    currency = RadioField('Select your currency:', choices=[
                          ('value', 'USD'), ('value_two', 'EUR')], default='value')
    buy_absolute = DecimalField(
        'Absolute (USD/EUR):', places=2, validators=[DataRequired()])
    buy_relative = DecimalField(
        'Relative (%):', places=2, validators=[DataRequired()])
    sell_absolute = DecimalField(
        'Absolute (USD/EUR):', places=2, validators=[DataRequired()])
    sell_relative = DecimalField(
        'Relative (%):', places=2, validators=[DataRequired()])
    recaptcha = RecaptchaField()
    simulate = SubmitField('Simulate')


class SearchForm(FlaskForm):
    q = StringField('Search blog', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)