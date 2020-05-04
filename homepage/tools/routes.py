
from flask import render_template, Blueprint, flash, redirect, url_for, request
from homepage.tools.forms import BT_GeneralForm, CorrelationMatrixForm
from homepage import login_required_author, db
from flask import request
from homepage.models import Portfolio, Position
from flask_login import login_user, current_user, logout_user
import sys
from homepage.stockinterface import getCorrelationMatrix
import numpy as np
import datetime as dt 
from homepage.utils import is_FormDataField_filled

tools = Blueprint('tools', __name__)


@tools.route('/correlation', methods=['GET', 'POST'])
@login_required_author()
def correlation():
    selectedPortfolio = request.args.get('selectedPortfolio', -1, type=int)

    form = CorrelationMatrixForm()
    portfolios = db.session.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()

    form.portfolios.choices = [(p.id,p.name) for p in portfolios]   

    if form.validate_on_submit():
        choosenPortfolioID = form.portfolios.data

        

        start = dt.datetime(1971,1,1)
        end = dt.datetime.now()

        if is_FormDataField_filled(form.startField.data) and is_FormDataField_filled(form.endField.data):
            start = form.startField.data
            end = form.endField.data
      
            
      
        # print ('Start  and End', file=sys.stderr )
        # print (start, file=sys.stderr )
        # print (end, file=sys.stderr )
        

        flash('We have computed the Correlation Matrix for you!', 'success')
        return redirect(url_for('tools.correlationResult', portfolio_id=choosenPortfolioID, start = start, end=end ))


    if selectedPortfolio >-1:
        form.portfolios.default = selectedPortfolio
        form.process()

    return render_template('correlation.html', title='Pandalike Investing - Correlation',form=form, selectedPortfolio=selectedPortfolio)


@tools.route('/correlation/result/<int:portfolio_id>/<date:start>/<date:end>', methods=['GET'])
def correlationResult(portfolio_id, start,end):


    tickers = [] 
    companyNames = []

    positions = db.session.query(Position).filter(Position.port_id == portfolio_id).all()
    for p in positions:
        tickers.append(p.ticker)
        companyNames.append(p.name)
    
    matrixMax = getCorrelationMatrix(tickers)


    

    showCustomMatrix = (start != dt.date(1971,1,1))
 

    if not showCustomMatrix:
        matrixCustom = matrixMax
    else:
        matrixCustom = getCorrelationMatrix(tickers,start,end)

    

    # matrix[0]= matrix[0].round(5)
    # print('Matrix',  file=sys.stderr)
    # print(matrix,  file=sys.stderr)
    # # print(res,  file=sys.stderr)

    
    return render_template('correlationResult.html', title='Pandalike Investing - Correlation Result', matrixMax = matrixMax, matrixCustom=matrixCustom, tickers = tickers, companyNames=companyNames, showCustomMatrix=showCustomMatrix)




@tools.route('/backtesting', methods=['GET', 'POST'])
@login_required_author(role="admin")
def backtesting():
    general_form = BT_GeneralForm()
    if request.method == 'POST':
        return render_template('backtesting.html', title='Pandalike Investing - Backtesting')
    else:
        return render_template('backtesting.html', general_form=general_form, title='Pandalike Investing - Backtesting')

