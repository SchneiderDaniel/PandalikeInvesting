from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_fontawesome import FontAwesome
from homepage.config import Config
import sys
from functools import wraps
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import  MenuLink
from flask_migrate import Migrate
from elasticsearch import Elasticsearch
from flask_babel import Babel
from flask import request
from datetime import datetime
from werkzeug.routing import BaseConverter, ValidationError


fa = FontAwesome()
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
admin = Admin()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'primary'
babel = Babel()

def login_required_author(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
              login_manager.login_message = u"Please log in to access this page."
              return login_manager.unauthorized()
            if not user_has_role(current_user,'admin'):
                if (not user_has_role(current_user, role) and (role != "ANY")):
                    login_manager.login_message = u"Your role has not enough priviledges to access this site. You need to upgrade your account."
                    return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def user_has_role (the_current_user, role):
    for the_user_role in the_current_user.roles:
        if (the_user_role.name == role): 
            return True
    return False

# https://stackoverflow.com/questions/31669864/date-in-flask-url
class DateConverter(BaseConverter):
    """Extracts a ISO8601 date from the path and validates it."""

    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError()

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')



def create_app(config_class=Config):
    print('Start creating the app',  file=sys.stderr)
    app = Flask(__name__)
    print('Start configure the app',  file=sys.stderr)
    # print(Config.RECAPTCHA_PUBLIC_KEY)
    # print(Config.RECAPTCHA_PRIVATE_KEY)
    # print(Config.SECRET_KEY)
    # print(Config.SQLALCHEMY_DATABASE_URI)
    # print(Config.MAIL_SERVER)
    # print(Config.MAIL_PORT)
    # print(Config.MAIL_USE_SSL)
    # print(Config.MAIL_USERNAME)
    # print(Config.MAIL_PASSWORD)
    # print(Config.ADMIN_MAIL)
    # print(Config.ADMIN_PASSWORD)
    # print(Config.ADMIN_NAME)
    # print(Config.ELASTICSEARCH_URL)
    # print(Config.IS_DEBUG)

    app.config.from_object(Config)

    app.url_map.converters['date'] = DateConverter

    app.jinja_env.globals.update(user_has_role=user_has_role)

    from homepage.users.routes import users
    from homepage.posts.routes import posts
    from homepage.main.routes import main
    from homepage.admins.routes import admins
    from homepage.tools.routes import tools
    from homepage.portfolios.routes import portfolios
    from homepage.errors.handlers import errors
    

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(admins)
    app.register_blueprint(tools)
    app.register_blueprint(portfolios)

    fa.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)
    babel.init_app(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    admin.init_app(app)
    admin.add_link(MenuLink(name='Go Back', category='', url='../'))

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None



    

    print('Done creating the app',  file=sys.stderr)
    return app



