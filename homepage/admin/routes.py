from flask import render_template, Blueprint, request, redirect, flash, url_for
from homepage import login_required_author
import sys
import bleach

admins = Blueprint('admins', __name__)


@login_required_author('admin')
@admins.route('/admin')
def admin():
    return render_template('admin.html')

@login_required_author('admin')
@admins.route('/send_newsletter', methods=['GET','POST'])
def send_newsletter():
    if request.method == 'POST':
        
        data = request.form.get('editordata')
        cleaned_data = bleach.clean(data, tags= ['h1','h2','h3','h4' ,'h5' ,'h6' , 'br', 'p','blockquote', 'b', 'u', 'pre', 'span', 'ul', 'li','ul', 'ol', 'a'  ])
        print(cleaned_data)

        flash('First you need to confirm', 'info')
        return redirect(url_for('admins.confirm_newsletter',data=cleaned_data))
    return render_template('newsletter.html')


@login_required_author('admin')
@admins.route('/confirm_newsletter', methods=['GET', 'POST'])
def confirm_newsletter():

    cleaned_data = request.args.get('data', 1, type=str)
    if request.method == 'POST':
        print(cleaned_data)
        flash('The Newsletter was sent out!', 'success')
        return (redirect(url_for('main.index')))


    return render_template('confirm_newsletter.html' , cleaned_data=cleaned_data )
