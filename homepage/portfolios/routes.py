from flask import render_template, Blueprint
from homepage.tools.forms import (BT_GeneralForm)
from homepage import login_required_author, db
from flask import request


portfolios = Blueprint('portfolios', __name__)


@portfolios.route('/portfolio/home')
def portfolio():
    return render_template('portfolio.html', title='Pandalike Investing - Portfolio')
