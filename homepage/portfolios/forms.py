from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, RadioField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange

from flask import render_template, Blueprint
from homepage import login_required_author, db
from flask import request


class CreatePortfolioForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=8,  max=20, message=('Your Portfolioname has to be between 8 and 30 characters.'))])
    numberPositions = IntegerField('Number of Positions', validators=[NumberRange(min=1,  max=100, message=('You can only create portfolios with 1 to 100 positions.'))] )
    recaptcha = RecaptchaField()
    submit = SubmitField('Create')