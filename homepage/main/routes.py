from flask import render_template, request, redirect, url_for, send_from_directory, flash, Blueprint, current_app
from homepage.main.forms import (ContactForm, BT_GeneralForm)
from homepage import login_required_author, db
import os
from homepage.models import Post, Tag, PostTags, User
from flask_login import current_user
import datetime
import random



main = Blueprint('main', __name__)


@main.route('/')
def index():

    randomPosts = []
    for i in range(0,3):
        query = db.session.query(Post)
        rowCount = int(query.count())
        randomRow = query.offset(int(rowCount*random.random())).first()
        randomPosts.append(randomRow)

        popularPosts = []

    randomTags = []
    for p in randomPosts:
        theTagRel = db.session.query(PostTags).filter(PostTags.post_id == p.id ).all()
        tagsPerPost= []
        for tr in theTagRel:
            tagToAdd = Tag.query.get_or_404(tr.tag_id)
            tagsPerPost.append(tagToAdd)
        randomTags.append(tagsPerPost)

        # popularPosts = Post.query.order_by(Post.comments.count()).limit(5).all()

        # popularPosts= db.session.query(Session, func.count(Run.id)).\
        #                         outerjoin(Run).\
        #                         group_by(Session.id).\
        #                         order_by(Session.id.desc())


        # db.session.query(Post, func.count(likes.c.user_id).label('total')).join(likes).group_by(Post).order_by('total DESC')
        # db.session.query(Post.comments.count()).label('total')).join(likes).group_by(Post).order_by('total DESC')

    return render_template('index.html', randomPosts = randomPosts, popularPosts=popularPosts, randomTags=randomTags)


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
    return render_template('about.html', title='About Me', showSidebar = False)


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

    return render_template('contact.html', contact_form=contact_form, title='Contact Us', userIsBanned = False, showSidebar = False)


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

@main.app_context_processor
def sidebar_tags():
    allTags = Tag.query.all()

    sizes = []
    for t in allTags:
        theTagRel = db.session.query(PostTags).filter(PostTags.tag_id == t.id ).all()
        sizes.append(len(theTagRel))

    return dict(allDBTags=allTags, tagSizes=sizes, showSidebar = True)

@main.app_context_processor
def bannedUser():
    if current_user.is_authenticated:
        user = User.query.get_or_404(current_user.id)
        if user.banned:
            return dict(userIsBanned = True)

    return dict(userIsBanned = False)


@main.app_context_processor
def year():
    current_year = datetime.datetime.now().year

    return dict(current_year = current_year) 