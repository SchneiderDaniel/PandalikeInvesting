from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BanUserForm(FlaskForm):
    name = StringField('Name:', [
        DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Ban/Unban')