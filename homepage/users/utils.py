import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from homepage import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/resources/img/profile_pics/' + picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
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
    msg.body = f''' Yout account was created. To activate your account, visit the following link:
{url_for('users.activate', token = token, _external = True)}

If you did not make this request, then simply ignore this E-Mail amd no changes will be made.
'''
    mail.send(msg)