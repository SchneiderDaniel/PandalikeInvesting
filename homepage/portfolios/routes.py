from flask import render_template, Blueprint
from homepage.tools.forms import (BT_GeneralForm)
from homepage import login_required_author, db
from flask import request


portfolios = Blueprint('portfolios', __name__)


@portfolios.route('/portfolio/home')
def portfolio():
    return render_template('portfolio.html', title='Pandalike Investing - Portfolio')


@portfolios.route('/portfolio/add_position')
def addPosition():
    return render_template('portfolio_addPostion.html', title='Pandalike Investing - Portfolio Add Position')


@portfolios.route('/portfolio/overview')
def overvie():
    return render_template('portfolio_Overview.html', title='Pandalike Investing - Portfolio Overview')
