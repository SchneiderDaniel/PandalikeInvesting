from flask import render_template, Blueprint, request, redirect
from homepage import login_required_author
import sys

admins = Blueprint('admins', __name__)


@login_required_author('admin')
@admins.route('/admin')
def admin():
    return render_template('admin.html')

@login_required_author('admin')
@admins.route('/send_newsletter')
def send_newsletter():
    return render_template('newsletter.html')