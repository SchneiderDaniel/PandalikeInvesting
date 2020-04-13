from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_fontawesome import FontAwesome
from homepage.config import Config

fa = FontAwesome()
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'primary'

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