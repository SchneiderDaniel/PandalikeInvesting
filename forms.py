from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField, TextAreaField, RadioField, DecimalField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo



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
    currency = RadioField('Select your currency:', choices=[('value','USD'),('value_two','EUR')], default='value')
    buy_absolute = DecimalField('Absolute (USD/EUR):', places=2, validators=[DataRequired()] )
    buy_relative = DecimalField('Relative (%):', places=2, validators=[DataRequired()] )
    sell_absolute = DecimalField('Absolute (USD/EUR):', places=2, validators=[DataRequired()] )
    sell_relative = DecimalField('Relative (%):', places=2, validators=[DataRequired()] )
    recaptcha = RecaptchaField()
    simulate = SubmitField('Simulate')


class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(),Length(min=6, max=20, message=('Username needs 6-20 characters.'))])
    email = StringField('E-Mail:', validators=[DataRequired(),Email()])
    password = PasswordField('Password:', validators=[DataRequired(),Length(min=8, message=('Password needs at least 8 characters'))])
    confirm_password = PasswordField('Confirm Password:',validators=[DataRequired(),EqualTo('password')])
    conditions = BooleanField('I accept the <a href="terms">Terms &amp; Conditions', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('E-Mail:', validators=[DataRequired(),Email()])
    password = PasswordField('Password:', validators=[DataRequired(),Length(min=8)])
    remember = BooleanField('Remember Me')
    recaptcha = RecaptchaField()
    submit = SubmitField('Login')