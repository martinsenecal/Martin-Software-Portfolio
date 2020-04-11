from flask import url_for, render_template, redirect, flash
from portfolio import app
from portfolio.forms import LoginForm  # Import Class Login
from portfolio.models import Post, Skill, User  # We need to put it here, since need to create db before.

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
@app.route('/home')
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

