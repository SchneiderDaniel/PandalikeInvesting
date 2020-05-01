from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, RadioField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, Email




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


class CorrelationMatrixForm(FlaskForm):
    portfolios = SelectField('Choose a Portfolio', coerce=int)
    recaptcha = RecaptchaField()
    submit = SubmitField('Compute')