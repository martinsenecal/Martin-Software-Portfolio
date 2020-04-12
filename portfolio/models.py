from datetime import datetime
from portfolio import db, login_manager
from flask_login import UserMixin  # Methods to help us deal with sessions.


# Extension to Help Login Manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Creation of Models for Database (similar to Class)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Way to Identify User.
    username = db.Column(db.String(20), unique=True, nullable=False)  # Unique Username and Mandatory.
    email = db.Column(db.String(100), unique=True, nullable=False)  # Unique Email and Mandatory.
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # Profile Pictures.
    password = db.Column(db.String(60), nullable=False)  # Hash Password
    posts = db.relationship('Post', backref='author', lazy=True)  # Load Data from the same user.

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(15), nullable=False)
    content = db.Column(db.String(80), nullable=False)
