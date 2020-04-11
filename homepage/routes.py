from flask import render_template, request, redirect, url_for, send_from_directory, flash
from homepage.forms import ContactForm, BT_GeneralForm, RegistrationForm, LoginForm, UpdateAccountForm
from homepage.models import User, Post
from homepage import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os
import sys

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'resources/img/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/blog')
def blog():
    return render_template('blog.html', title = 'Blog')

@app.route('/terms')
def terms():
    return render_template('terms.html', title = 'Terms &amp; Conditions')

@app.route('/about')
def about():
    return render_template('about.html', title = 'About Me')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', title = 'Pricing')

@app.route('/correlation')
def correlation():
    return render_template('correlation.html', title = 'Correlation')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
        user = User(username = register_form.username.data, email = register_form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {register_form.email.data}! You are now able to login', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', register_form=register_form, title = 'Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
   

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,login_form.password.data):
            login_user(user,remember = login_form.remember.data)
            next_page = request.args.get('next')            
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash ('Login Unsuccessful. Please check mail and password', 'danger')
    
    return render_template('login.html', login_form=login_form, title = 'Login')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        flash(f'Thanks {contact_form.name.data}, we have received your meessage. We will respond soon!', 'success')
        return redirect(url_for('index'))
    
    return render_template('contact.html', contact_form=contact_form, title = 'Contact Us')

@app.route('/backtesting', methods=['GET', 'POST'])
@login_required
def backtesting():
    general_form = BT_GeneralForm()
    if request.method == 'POST':
        return render_template('backtesting.html')
    else:
        return render_template('backtesting.html', general_form=general_form, title = 'Backtesting')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    updateAccount_form = UpdateAccountForm()
    if updateAccount_form.validate_on_submit():
        current_user.username = updateAccount_form.username.data
        current_user.email = updateAccount_form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        updateAccount_form.username.data = current_user.username
        updateAccount_form.email.data = current_user.email
    image_file = url_for('static', filename='resources/img/profile_pics/' + current_user.image_file )
    return render_template('account.html', title = 'Account', image_file = image_file, updateAccount_form=updateAccount_form)