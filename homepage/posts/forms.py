from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(
        max=100, message=('Title is limited to 100 characters.'))])
    content = TextAreaField('Content', [DataRequired(), Length(min=8, message=(
        'Your message is too short. It needs at least 8 characters.'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Post')
