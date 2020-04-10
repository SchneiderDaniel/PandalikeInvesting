from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime
import os
import sys
from forms import ContactForm
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome


# RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
# RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'


app = Flask(__name__)
fa = FontAwesome(app)
Bootstrap(app)

app.config.from_mapping(SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
app.config.from_object(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'resources/img/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/backtesting', methods=['GET', 'POST'])
def visualization():
    if request.method == 'POST':
        return render_template('backtesting.html')
    else:
        return render_template('backtesting.html')

@app.route('/contact', methods=('GET', 'POST'))
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        print('POSTI!', file=sys.stderr)
        print(form.name, file=sys.stderr)
        print(form.email, file=sys.stderr)
        print(form.body, file=sys.stderr)
        return redirect(url_for('success'))
    else:
        print('Get!', file=sys.stderr)
        return render_template('contact.html', form=form)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True)




#  print('POSTI!', file=sys.stderr)