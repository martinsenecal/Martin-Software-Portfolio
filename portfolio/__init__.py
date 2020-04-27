from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from portfolio.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

# Login Manager (by Flask) to take care of all the users session.
login_manager = LoginManager()  # Handle all the session for us in the background.
login_manager.login_view = 'users.login'  # Redirect to Login if not already login.
login_manager.login_message_category = 'info'  # Style for Error Message - already defined (Bootstrap Class)

# Email
mail = Mail()


def create_app(config_class=Config):
    # Creation of the Project
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Avoid Circular Import: BluePrint
    from portfolio.users.routes import users
    from portfolio.posts.routes import posts
    from portfolio.main.routes import main
    from portfolio.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app