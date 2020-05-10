from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, Field, RadioField
from wtforms.widgets import  TextInput, html_params
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100, message=('Title is limited to 100 characters.'))])
    abstract = TextAreaField('Abstract', [DataRequired(), Length(min=8,  max=150, message=('Your abstract has to be between 8 and 150 characters.'))])
    content = TextAreaField('Content', [DataRequired(), Length(min=8, message=('Your message is too short. It needs at least 8 characters.'))])
    region = RadioField('Region', coerce=int, default = 0, choices=[(0,'World'),(1,'Europe'),(2,'Germany')])
    tags = StringField('Tags', [DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Content', [DataRequired(), Length(min=8,max=150, message=('Your message needs to be 8 to 150 characters long.'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Comment')

class DiscussionForm(FlaskForm):
    content = TextAreaField('Content', [DataRequired(), Length(max=150, message=('Your message is too large. Max is 150 characters.'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Send')


class ReportForm(FlaskForm):
    complain = TextAreaField('Reason?', [DataRequired(), Length(min=8,max=150, message=('Your message needs to be 8 to 150 characters long.'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Report')