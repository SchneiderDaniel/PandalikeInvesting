#Libs
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy
import os
import sys

# RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
# RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
# DEV (Don't use for PROD)
RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
app = Flask(__name__)
fa = FontAwesome(app)
Bootstrap(app)
# DEV (Don't use for PROD)
app.config.from_mapping(SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
# app.config.from_mapping(SECRET_KEY=os.getenv('SECRET_PUBLIC_KEY'))
app.config.from_object(__name__)
# DEV (Don't use for PROD)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


from homepage import routes