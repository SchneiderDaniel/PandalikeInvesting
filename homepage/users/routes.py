from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, current_user, logout_user
from homepage.models import User, Post, Role, UserRoles
from homepage import db, bcrypt
from homepage.users.forms import (RegistrationForm,
                                  LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, ActivateAccountForm)
from homepage.users.utils import save_picture, sendResetEMail, sendActivateEMail
from homepage import login_required_author


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            register_form.password.data).decode('utf-8')
        user = User(username=register_form.username.data,
                    email=register_form.email.data, password=hashed_password)
        user.roles.append(Role.query[0])
        db.session.add(user)
        db.session.commit()
        sendActivateEMail(user)
        flash(
            f'Account created for {register_form.email.data}! Plz check your mails for activating your account.', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', register_form=register_form, title='Register')


@users.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        
            
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            if not user.activated:
                flash('Your account data is correct but your account is not activated. Check your mails.', 'danger')
            else:
                login_user(user, remember=login_form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check mail and password', 'danger')

    return render_template('login.html', login_form=login_form, title='Login')


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/account', methods=['GET', 'POST'])
@login_required_author()
def account():
    updateAccount_form = UpdateAccountForm()
    if updateAccount_form.validate_on_submit():
        if updateAccount_form.picture.data:
            picture_file = save_picture(updateAccount_form.picture.data)
            current_user.image_file = picture_file
        current_user.username = updateAccount_form.username.data
        current_user.email = updateAccount_form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        updateAccount_form.username.data = current_user.username
        updateAccount_form.email.data = current_user.email
    image_file = url_for(
        'static', filename='resources/img/profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, updateAccount_form=updateAccount_form)


@users.route('/user/<string:username>')
def user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    image_file = url_for(
        'static', filename='resources/img/profile_pics/' + user.image_file)
    return render_template('user.html', title='Blog', posts=posts, user=user, image_file=image_file)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        sendResetEMail(user)
        flash('An E-Mail has been send with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'The password has been reset! You are now able to login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route('/activate/<token>', methods=['GET'])
def activate(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.activate_account'))
    
    if user.activated 
        flash('Your account is already activated.', 'info')
        redirect(url_for('users.login'))

    user.activated = True
    db.session.commit()
    flash(f'Your account has been activated. You can now log in.', 'success')
    return redirect(url_for('users.login'))


@users.route('/activate_account', methods=['GET', 'POST'])
def activate_account():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ActivateAccountForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.activated 
            flash('Your account is already activated.', 'info')
            return redirect(url_for('users.login'))
        sendActivateEMail(user)
        flash(f'The activation mail was send out again', 'info')
        return redirect(url_for('users.login'))

    return render_template('activate_account.html', title='Activate Account', form=form)