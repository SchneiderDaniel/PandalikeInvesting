from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, TextField, SubmitField, TextAreaField, RadioField, DecimalField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from homepage.models import User

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

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already used. Please choose a different one.')
    
    def validate_email(self,email):
        mail = User.query.filter_by(email=email.data).first()
        if mail:
            raise ValidationError('That E-Mail is already used. Please choose a different one.')

    

class LoginForm(FlaskForm):
    email = StringField('E-Mail:', validators=[DataRequired(),Email()])
    password = PasswordField('Password:', validators=[DataRequired(),Length(min=8)])
    remember = BooleanField('Remember Me')
    recaptcha = RecaptchaField()
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(),Length(min=6, max=20, message=('Username needs 6-20 characters.'))])
    email = StringField('E-Mail:', validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png ', 'gif'])])
    recaptcha = RecaptchaField()
    submit = SubmitField('Update')

  

    def validate_username(self,username):
        if (username.data!=current_user.username):
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already used. Please choose a different one.')
    
    def validate_email(self,email):
        if (email.data!=current_user.email):
            mail = User.query.filter_by(email=email.data).first()
            if mail:
                raise ValidationError('That E-Mail is already used. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(max=100, message=('Title is limited to 100 characters.'))])
    content = TextAreaField('Content', [DataRequired(), Length(min=8, message=('Your message is too short. It needs at least 8 characters.'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
    email = StringField('E-Mail:', validators=[DataRequired(),Email()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account for this E-Mail. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password:', validators=[DataRequired(),Length(min=8, message=('Password needs at least 8 characters'))])
    confirm_password = PasswordField('Confirm Password:',validators=[DataRequired(),EqualTo('password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Reset my password')