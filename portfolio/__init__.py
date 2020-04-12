from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# Secret Key
app.config['SECRET_KEY'] = 'SDF3W478_HS3ish34'
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)  # Handle all the session for us in the background.
login_manager.login_view = 'login'  # Redirect to Login if not already login.
login_manager.login_message_category = 'info'  # Style for Error Message - already defined (Bootstrap Class)

# Avoid Circular Import
from portfolio import routes
