from flask import render_template, request, redirect, url_for, send_from_directory, flash
from homepage.forms import ContactForm, BT_GeneralForm, RegistrationForm, LoginForm
from homepage.models import User, Post
from homepage import app, db, bcrypt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'resources/img/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/correlation')
def correlation():
    return render_template('correlation.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
        user = User(username = register_form.username.data, email = register_form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {register_form.email.data}! You are now able to login', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', register_form=register_form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == 'admin@blog.com' and login_form.password.data == 'qweqweqwe':
            flash(f'Logged in as {login_form.email.data}!', 'success')
            return redirect(url_for('index'))
        else:
            flash ('Login Unsuccessful. Please check mail and password', 'danger')
        

    return render_template('login.html', login_form=login_form)

@app.route('/contact', methods=('GET', 'POST'))
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        flash(f'Thanks {contact_form.name.data}, we have received your meessage. We will respond soon!', 'success')
        return redirect(url_for('index'))
    
    return render_template('contact.html', contact_form=contact_form)

@app.route('/backtesting', methods=['GET', 'POST'])
def backtesting():
    general_form = BT_GeneralForm()
    if request.method == 'POST':
        return render_template('backtesting.html')
    else:
        return render_template('backtesting.html', general_form=general_form)