from flask import render_template, request, redirect, url_for, send_from_directory, flash, Blueprint, current_app
from homepage.main.forms import (ContactForm, SearchForm)
from homepage import login_required_author, db
import os
from homepage.models import Post, Tag, PostTags, User
from flask_login import current_user
from datetime import datetime
import random
from flask import g
from flask_babel import Babel, get_locale
import urllib
from markupsafe import Markup
from homepage.users.utils import sendEMailToAdmin


main = Blueprint('main', __name__)


@main.route('/')
def index():

    randomPosts = []

    if(len(db.session.query(Post).all())>0):
        for i in range(0,3):
            query = db.session.query(Post)
            rowCount = int(query.count())
            randomRow = query.offset(int(rowCount*random.random())).first()
            randomPosts.append(randomRow)

           

    randomTags = []

    if(len(db.session.query(Post).all())>0):
        for p in randomPosts:
            theTagRel = db.session.query(PostTags).filter(PostTags.post_id == p.id ).all()
            tagsPerPost= []
            for tr in theTagRel:
                tagToAdd = Tag.query.get_or_404(tr.tag_id)
                tagsPerPost.append(tagToAdd)
            randomTags.append(tagsPerPost)

    return render_template('index.html', randomPosts = randomPosts, randomTags=randomTags, shareable=True)


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'resources/img/favicon.ico', mimetype='image/vnd.microsoft.icon')


@main.route('/terms')
def terms():
    return render_template('terms.html', title='Pandalike Investing - Terms &amp; Conditions')

@main.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Pandalike Investing - Privacy Policy')

@main.route('/legal')
def legal_notice():
    return render_template('legal_notice.html', title='Pandalike Investing - Impressum - Legal Notice')


@main.route('/about')
def about():
    return render_template('about.html', title='Pandalike Investing - About Me', showSidebar = False, shareable=True)


# @main.route('/pricing')
# def pricing():
#     return render_template('pricing.html', title='Pandalike Investing - Pricing', shareable=True)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():

        sendEMailToAdmin(contact_form.email.data,contact_form.name.data,contact_form.body.data)
        flash(
            f'Thanks {contact_form.name.data}, we have received your message. We will respond soon!', 'success')
        return redirect(url_for('main.index'))

    return render_template('contact.html', contact_form=contact_form, title='Pandalike Investing - Contact Us', userIsBanned = False, showSidebar = False, shareable=True)

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
    current_year = datetime.now().year

    return dict(current_year = current_year) 

@main.app_context_processor
def urlAndTitleInject():

    return dict(url = request.url, title ="Pandalike Investing", shareable = False, isDebug=current_app.config['DEBUG']) 


@main.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@main.route('/search')
@login_required_author()
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Pandalike Investing - Search', posts=posts.all(),
                           next_url=next_url, prev_url=prev_url)



@main.app_template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.parse.quote_plus(s)
    return Markup(s)