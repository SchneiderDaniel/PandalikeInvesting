from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email



class ContactForm(FlaskForm):
    """Contact form."""
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