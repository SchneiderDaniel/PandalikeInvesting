from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField, TextAreaField, RadioField, DecimalField
from wtforms.validators import DataRequired, Length, Email



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
    currency = RadioField('Select your currency:', choices=[('value','USD'),('value_two','EUR')])
    buy_absolute = DecimalField('Absolute (USD/EUR):', places=2, validators=[DataRequired()] )
    buy_relative = DecimalField('Relative (%):', places=2, validators=[DataRequired()] )
    sell_absolute = DecimalField('Absolute (USD/EUR):', places=2, validators=[DataRequired()] )
    sell_relative = DecimalField('Relative (%):', places=2, validators=[DataRequired()] )