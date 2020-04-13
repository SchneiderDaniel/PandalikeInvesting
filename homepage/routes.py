from flask import render_template, request, redirect, url_for, send_from_directory, flash, abort
from homepage.forms import ContactForm, BT_GeneralForm, RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from homepage.models import User, Post
from homepage import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os
import sys
import secrets
from PIL import Image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'resources/img/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    posts = Post.query.all()
    return render_template('blog.html', title = 'Blog', posts=posts)

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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/resources/img/profile_pics/' + picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn    

@app.route('/account', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        updateAccount_form.username.data = current_user.username
        updateAccount_form.email.data = current_user.email
    image_file = url_for('static', filename='resources/img/profile_pics/' + current_user.image_file )
    return render_template('account.html', title = 'Account', image_file = image_file, updateAccount_form=updateAccount_form)


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog'))
    return render_template('new_post.html', title = 'New post', form = form, legend ='New Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post = post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'] )
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return (redirect(url_for('post', post_id = post.id)))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new_post.html', title = 'Update Post', form = form, legend ='Update Post')


@app.route('/post/<int:post_id>/delete', methods=['POST'] )
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return (redirect(url_for('blog', post_id = post.id)))
