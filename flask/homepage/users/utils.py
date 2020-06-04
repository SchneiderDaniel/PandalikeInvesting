import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from homepage import mail, db
from homepage.models import Newsletter, User
import sys


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/resources/img/profile_pics/' + picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    if i.mode != 'RGB':
        i = i.convert('RGB')
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def sendResetEMail(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token = token, _external = True)}

If you did not make this request, then simply ignore this E-Mail amd no changes will be made.
'''
    mail.send(msg)


def sendActivateEMail(user):
    token = user.get_reset_token()
    msg = Message('Activate Account Mail',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f''' Your account was created. To activate your account, visit the following link:
{url_for('users.activate', token = token, _external = True)}

If you did not make this request, then simply ignore this E-Mail amd no changes will be made.
'''
    mail.send(msg)

def sendNewsletter(nl_id):
    nl = Newsletter.query.get_or_404(nl_id)
    users = db.session.query(User).filter(User.newsletter == True ).all()

    mailingList = []
    for u in users:
        mailingList.append(u.email)

    # print('Mailing List', file=sys.stderr)
    # print(mailingList, file=sys.stderr)
    # print(len(mailingList),file=sys.stderr)

    if len(mailingList)>0:
        msg = Message(nl.title,sender=current_app.config['MAIL_USERNAME'],recipients=mailingList)
        
        url = '<a href="' + str(url_for('users.account',_external = True)) + '" >Here</a> '
        footer = '<br> <br> Are you no longer interested in the Newsletter? Just sign off '
        msg.body = ''
        msg.html = nl.content + footer + url
        # print(url, file=sys.stderr)

        mail.send(msg)
        # print('Mail send out', file=sys.stderr)