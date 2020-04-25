from flask import render_template, Blueprint, request, redirect, flash, url_for
from homepage import login_required_author, db
import sys
import bleach
from homepage.models import Newsletter, User, Report, Comment
from homepage.users.utils import sendNewsletter
from homepage.admins.forms import BanUserForm

admins = Blueprint('admins', __name__)


@login_required_author('admin')
@admins.route('/banUser', methods=['GET','POST'])
def banUser():
    form = BanUserForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.name.data ).first()
        if not user:
            flash('This user was not found in the database', 'danger')
            return redirect(url_for('admins.banUser'))
        if user.banned:
            user.banned = False
            db.session.commit()
            flash('This user is not longer banned', 'success')
        else:
            user.banned = True
            db.session.commit()
            flash('This user has been banned', 'success')
        
        return redirect(url_for('admins.banUser'))


    return render_template('banUser.html', showSidebar = False, form = form)

@login_required_author('admin')
@admins.route('/send_newsletter', methods=['GET','POST'])
def send_newsletter():
    if request.method == 'POST':
        
        data = request.form.get('editordata')
    

        # print(data,  file=sys.stderr)

        # allowed_tags = ['class', 'div', 'img', 'h1', 'h2','src' ,'h3','h4' ,'h5' ,'h6' , 'br', 'p','blockquote', 'b', 'u', 'pre', 'span', 'ul', 'li','ul', 'ol', 'a', 'abbr', 'acronym', 'code',
        #                 'em', 'i', 'pre', 'strong', 'video',  'iframe', 'hr', 'style', 'font' ]
        # allowed_attrs = {'*': ['class'],
        #                 'a': ['href', 'rel'],
        #                 'img': ['src', 'alt', 'data-filename','style' , 'width'],
        #                 'font': ['color']}


        # cleaned_data = bleach.clean(data, tags=allowed_tags,attributes=allowed_attrs, protocols=['data'], styles=['width','background','font-family', 'text-align' ])


        cleaned_data = data
        # print(data,  file=sys.stderr)
        # print('____________',  file=sys.stderr)
        # print(cleaned_data,  file=sys.stderr)

        title = request.form.get('title')
        nl = Newsletter(title=title, content=cleaned_data)
        db.session.add(nl)
        db.session.commit()

        flash('First you need to confirm the newsletter', 'info')
        return redirect(url_for('admins.confirm_newsletter',nl_id=nl.id))
    return render_template('newsletter.html', showSidebar = False)


@login_required_author('admin')
@admins.route('/confirm_newsletter/<int:nl_id>', methods=['GET', 'POST'])
def confirm_newsletter(nl_id):

    nl = Newsletter.query.get_or_404(nl_id)

    if request.method == 'POST':

        sendNewsletter(nl_id)
        flash('The newsletter has been sent out!', 'success')
        return (redirect(url_for('main.index')))
    
    return render_template('confirm_newsletter.html' , nl_content=nl.content, nl_title = nl.title, showSidebar = False )


@login_required_author('admin')
@admins.route('/report_Dashboard', methods=['GET', 'POST'])
def report_Dashboard():

    reports = db.session.query(Report).all()
    comments = []
    for r in reports:
        comment = Comment.query.get_or_404(r.cid)
        comments.append(comment)
    
    return render_template('reportDash.html' , showSidebar = False, reports=reports, comments = comments )

@login_required_author('admin')
@admins.route('/testPage')
def testPage():
    return render_template('test.html', title='Test Page')