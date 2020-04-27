# Import
from flask import url_for, render_template, redirect, flash
from flask import current_app
from portfolio.main.forms import ResumeForm
from portfolio.models import Skill  # We need to put it here, since need to create db before.
from flask_mail import Message
from portfolio import mail
from flask import Blueprint

main = Blueprint('main', __name__)


# Routes
@main.route('/about')
def about():
    return render_template("about.html")


@main.route('/')
@main.route('/home')
def homepage():
    return render_template("home.html")


@main.route('/skills')
def skills():
    skills_content = Skill.query.all()  # Query of all the skills in the database
    return render_template("skills.html", skills=skills_content)  # Returning skills content inside the templates


@main.route('/experience')
def education():
    return render_template("experience.html")


@main.route('/egg')
def easteregg():
    return render_template("game.html")


@main.route('/projects')
def projects():
    return render_template("projects.html")


@main.route("/connect", methods=['GET', 'POST'])
def connect():
    formResume = ResumeForm()  # Creation of the Form
    if formResume.validate_on_submit():
        email = formResume.email.data
        with current_app.app_context():
            msg = Message(subject="Martin - Resume (Software Engineering Student)",
                          sender=current_app.config.get("MAIL_USERNAME"),
                          recipients=[email],
                          body="Hello! I'm glad you ask for my resume. Here is the link: www.google.com")
            mail.send(msg)
        flash("The resume was sent! Let's connect!", 'success')
        return redirect(url_for('main.connect'))
    return render_template('connect.html', formResume=formResume)
