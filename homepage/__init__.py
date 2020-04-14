from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_fontawesome import FontAwesome
from homepage.config import Config
import sys
from functools import wraps

fa = FontAwesome()
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'primary'

def login_required_author(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
              login_manager.login_message = u"Please log in to access this page."
              return login_manager.unauthorized()
            if (current_user.roles[0].name != "admin"):  
                if ((current_user.roles[0].name != role) and (role != "ANY")):
                    login_manager.login_message = u"Your role has not enough priviledges to access this site. You need to upgrade your account."
                    return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from homepage.users.routes import users
    from homepage.posts.routes import posts
    from homepage.main.routes import main
    from homepage.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    fa.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    return app
