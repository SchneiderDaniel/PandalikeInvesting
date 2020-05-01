from flask import render_template, request, redirect, url_for, flash, Blueprint
from homepage import login_required_author, db
from flask_login import login_user, current_user, logout_user
from flask import request
from homepage.portfolios.forms import CreatePortfolioForm, EditPositionForm
from homepage.models import Portfolio, Position
import yfinance as yf
import sys

from homepage.stockinterface import getNameToTicker

portfolios = Blueprint('portfolios', __name__)

@login_required_author()
@portfolios.route('/portfolio/home', methods=['GET', 'POST'])
def portfolio():

    form = CreatePortfolioForm()
    if form.validate_on_submit():

        portfolio = Portfolio(name=form.name.data, numberPositions=form.numberPositions.data, user_id=current_user.id)
        
        db.session.add(portfolio)
        db.session.commit()

        for i in range(0,portfolio.numberPositions):
            position = Position(port_id=portfolio.id)
            db.session.add(position)

        db.session.commit()

        flash('Your portfolio has been created!', 'success')
        return redirect(url_for('portfolios.portfolio'))

    portfolios = db.session.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()

    return render_template('portfolio.html', title='Pandalike Investing - Portfolio', form = form, portfolios=portfolios)

@login_required_author()
@portfolios.route('/portfolio/edit_position/<int:portfolio_id>/<int:position_id>', methods=['GET', 'POST'])
def editPosition(portfolio_id,position_id):

    form = EditPositionForm()

    portfolio = Portfolio.query.filter_by(id=portfolio_id).first_or_404()
    if portfolio.creator != current_user:
            abort(403)
    position = Position.query.filter_by(id=position_id).first_or_404()

    if form.validate_on_submit():  
        position.name = getNameToTicker(form.ticker.data)
        position.ticker = form.ticker.data
        position.percent = form.percent.data 
        db.session.commit()

        flash('Your position has been updated!', 'success')
        return redirect(url_for('portfolios.overview', portfolio_id=portfolio_id))

    elif request.method == 'GET':
        form.name.data = position.name
        form.ticker.data = position.ticker
        form.percent.data = position.percent


    return render_template('portfolio_editPosition.html', title='Pandalike Investing - Portfolio Edit Position', portfolio=portfolio, position=position, form=form)

@login_required_author()
@portfolios.route('/portfolio/overview/<int:portfolio_id>',  methods=['GET', 'POST'])
def overview(portfolio_id):

    portfolio = Portfolio.query.filter_by(id=portfolio_id).first_or_404()

    if portfolio.creator != current_user:
        abort(403)
    positions = db.session.query(Position).filter(Position.port_id == portfolio_id).all()


    return render_template('portfolio_Overview.html', title='Pandalike Investing - Portfolio Overview', portfolio=portfolio, positions = positions)
