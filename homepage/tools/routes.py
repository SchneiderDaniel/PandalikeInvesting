
from flask import render_template, Blueprint
from homepage.tools.forms import (BT_GeneralForm)
from homepage import login_required_author, db
from flask import request


tools = Blueprint('tools', __name__)


@tools.route('/correlation')
def correlation():
    return render_template('correlation.html', title='Pandalike Investing - Correlation')



@tools.route('/backtesting', methods=['GET', 'POST'])
@login_required_author(role="admin")
def backtesting():
    general_form = BT_GeneralForm()
    if request.method == 'POST':
        return render_template('backtesting.html', title='Pandalike Investing - Backtesting')
    else:
        return render_template('backtesting.html', general_form=general_form, title='Pandalike Investing - Backtesting')

