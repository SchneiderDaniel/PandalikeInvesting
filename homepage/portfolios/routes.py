from flask import render_template, request, redirect, url_for, flash, Blueprint
from homepage import login_required_author, db
from flask_login import login_user, current_user, logout_user
from flask import request
from homepage.portfolios.forms import CreatePortfolioForm
from homepage.models import Portfolio


portfolios = Blueprint('portfolios', __name__)

@login_required_author()
@portfolios.route('/portfolio/home', methods=['GET', 'POST'])
def portfolio():

    form = CreatePortfolioForm()
    if form.validate_on_submit():

        portfolio = Portfolio(name=form.name.data, numberPositions=form.numberPositions.data, user_id = current_user.id)
        
        db.session.add(portfolio)
        db.session.commit()

        flash('Your portfolio has been created!', 'success')
        return redirect(url_for('portfolios.portfolio'))

    portfolios = db.session.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()

    return render_template('portfolio.html', title='Pandalike Investing - Portfolio', form = form, portfolios=portfolios)

@login_required_author()
@portfolios.route('/portfolio/add_position')
def addPosition():
    return render_template('portfolio_addPostion.html', title='Pandalike Investing - Portfolio Add Position')

@login_required_author()
@portfolios.route('/portfolio/overview/<int:portfolio_id>',  methods=['GET', 'POST'])
def overview(portfolio_id):
    return render_template('portfolio_Overview.html', title='Pandalike Investing - Portfolio Overview')
