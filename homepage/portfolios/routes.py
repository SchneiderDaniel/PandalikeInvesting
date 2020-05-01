from flask import render_template, request, redirect, url_for, flash, Blueprint
from homepage import login_required_author, db
from flask import request
from homepage.portfolios.forms import CreatePortfolioForm


portfolios = Blueprint('portfolios', __name__)

@login_required_author()
@portfolios.route('/portfolio/home', methods=['GET', 'POST'])
def portfolio():

    form = CreatePortfolioForm()
    if form.validate_on_submit():

        flash('Your portfolio has been created!', 'success')
        return redirect(url_for('portfolios.portfolio'))

    return render_template('portfolio.html', title='Pandalike Investing - Portfolio', form = form)

@login_required_author()
@portfolios.route('/portfolio/add_position')
def addPosition():
    return render_template('portfolio_addPostion.html', title='Pandalike Investing - Portfolio Add Position')

@login_required_author()
@portfolios.route('/portfolio/overview')
def overvie():
    return render_template('portfolio_Overview.html', title='Pandalike Investing - Portfolio Overview')
