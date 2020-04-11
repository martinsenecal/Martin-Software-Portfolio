from datetime import datetime
from flask import Flask, url_for, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm  # Import Class Login

app = Flask(__name__)
# Secret Key
app.config['SECRET_KEY'] = 'SDF3W478_HS3ish34'
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# Creation of Models for Database (similar to Class)
class User(db.Model):
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


posts = [
    {'author': 'Martin Senecal',
     'title': 'My First Blog Post',
     'content': 'This the first content of my Blog',
     'date_posted': 'April 11, 2020'
     },
    {'author': 'Martin Senecal',
     'title': 'My Second Article',
     'content': 'This the second article of my Blog',
     'date_posted': 'April 13, 2020'
     }
]


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/skills')
def skills():
    return render_template("skills.html")


@app.route('/experience')
def education():
    return render_template("experience.html")


@app.route('/projects')
def projects():
    return render_template("projects.html")


@app.route('/connect')
def connect():
    return render_template("connect.html")


@app.route('/blog')
def blog():
    return render_template("blog.html", posts=posts)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create Object Login
    if form.validate_on_submit():
        if form.email.data == 'admin@martin.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')  # (message, bootstrap class)
            return redirect(url_for('homepage'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
