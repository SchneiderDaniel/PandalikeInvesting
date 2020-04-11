from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from datetime import datetime
import os
import sys
from forms import ContactForm, BT_GeneralForm, RegistrationForm, LoginForm
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome


# RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
# RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'


app = Flask(__name__)
fa = FontAwesome(app)
Bootstrap(app)

app.config.from_mapping(SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
# app.config.from_mapping(SECRET_KEY=os.getenv('SECRET_PUBLIC_KEY'))
app.config.from_object(__name__)


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
        flash(f'Account created for {register_form.email.data}!', 'success')
        return redirect(url_for('index'))
    
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
        flash(f'Thanks {contact_form.name.data}, we received your meessage. We will respond soon!', 'success')
        return redirect(url_for('index'))
    
    return render_template('contact.html', contact_form=contact_form)

@app.route('/backtesting', methods=['GET', 'POST'])
def backtesting():
    general_form = BT_GeneralForm()
    if request.method == 'POST':
        return render_template('backtesting.html')
    else:
        return render_template('backtesting.html', general_form=general_form)

if __name__ == "__main__":
    app.run(debug=True)




#  print('POSTI!', file=sys.stderr)