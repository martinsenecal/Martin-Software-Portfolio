# Import
from flask import url_for, render_template, redirect, flash, request
from portfolio import db, bcrypt
from portfolio.users.forms import LoginForm, UpdateAdminForm
from portfolio.models import Skill, User  # We need to put it here, since need to create db before.
from flask_login import login_user, current_user, logout_user, login_required  # Function that come from login manager.
from flask import Blueprint
from portfolio.users.utils import save_picture

users = Blueprint('users', __name__)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # Redirect to Admin after LogIn (Optional)
            return redirect(next_page) if next_page else redirect(url_for('main.homepage'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')  # (message, bootstrap class)

    return render_template('login.html', form=form)


@users.route("/logout")
def logout():
    logout_user()  # Method from LoginManager
    return redirect(url_for('main.homepage'))


@users.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    users = User.query.all()
    form = UpdateAdminForm()
    if form.validate_on_submit():
        # Resizing of the User Picture with Pillow
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data

        # If Skill field is empty, it won't be add to the DB
        if form.skillName.data != "":
            skill = Skill(type='Soft', content=form.skillName.data)
            db.session.add(skill)

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.admin'))
    elif request.method == 'GET':
        # Show some data already in the fields when user is making a get-request.
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.skillName.data = ""

    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)  # Location of the Image in Static Folder

    return render_template('admin.html', image_file=image_file, form=form, users=users)
