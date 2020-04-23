from flask import render_template, Blueprint, request, redirect, flash, url_for
from homepage import login_required_author, db
import sys
import bleach
from homepage.models import Newsletter

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
        
        title = request.form.get('title')
        nl = Newsletter(title=title, content=cleaned_data)
        db.session.add(nl)
        db.session.commit()

        flash('First you need to confirm', 'info')
        return redirect(url_for('admins.confirm_newsletter',nl_id=nl.id))
    return render_template('newsletter.html')


@login_required_author('admin')
@admins.route('/confirm_newsletter/<int:nl_id>', methods=['GET', 'POST'])
def confirm_newsletter(nl_id):

    nl = Newsletter.query.get_or_404(nl_id)

    if request.method == 'POST':
        print('title: ' + nl.title, file=sys.stderr)
        print('Content: ' + nl.content, file=sys.stderr)
        flash('The Newsletter was sent out!', 'success')
        return (redirect(url_for('main.index')))
    
    return render_template('confirm_newsletter.html' , nl_content=nl.content, nl_title = nl.title )
