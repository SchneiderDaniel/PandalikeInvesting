from flask import render_template, request, redirect, url_for, send_from_directory, flash, Blueprint, current_app
from homepage.main.forms import (ContactForm, BT_GeneralForm)
from homepage import login_required_author, db
import os
from homepage.models import Post


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'resources/img/favicon.ico', mimetype='image/vnd.microsoft.icon')





@main.route('/terms')
def terms():
    return render_template('terms.html', title='Terms &amp; Conditions')

@main.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy Policy')

@main.route('/legal')
def legal_notice():
    return render_template('legal_notice.html', title='Impressum - Legal Notice')


@main.route('/about')
def about():
    return render_template('about.html', title='About Me')


@main.route('/pricing')
def pricing():
    return render_template('pricing.html', title='Pricing')


@main.route('/correlation')
def correlation():
    return render_template('correlation.html', title='Correlation')


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        flash(
            f'Thanks {contact_form.name.data}, we have received your meessage. We will respond soon!', 'success')
        return redirect(url_for('main.index'))

    return render_template('contact.html', contact_form=contact_form, title='Contact Us')


@main.route('/backtesting', methods=['GET', 'POST'])
@login_required_author(role="admin")
def backtesting():
    general_form = BT_GeneralForm()
    if request.method == 'POST':
        return render_template('backtesting.html')
    else:
        return render_template('backtesting.html', general_form=general_form, title='Backtesting')


@main.app_context_processor
def inject_template_scope():
    injections = dict()

    def cookies_check():
        value = request.cookies.get('cookie_consent')
        return value == 'true'
    injections.update(cookies_check=cookies_check)

    return injections