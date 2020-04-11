from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Secret Key
app.config['SECRET_KEY'] = 'SDF3W478_HS3ish34'
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Avoid Circular Import
from portfolio import routes
