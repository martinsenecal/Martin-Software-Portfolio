import os  # for extension of files type.
import secrets  # for Random String.
from PIL import Image  # Pillow resize pictures to take less space in DB (Image is a class from Pillow Library)
from flask import url_for, render_template, redirect, flash, request, abort
from portfolio import app, db, bcrypt
from portfolio.forms import LoginForm, UpdateAdminForm, PostForm  # Import Class Login
from portfolio.models import Post, Skill, User  # We need to put it here, since need to create db before.
from flask_login import login_user, current_user, logout_user, login_required  # Function that come from login manager.


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/')
@app.route('/home')
def homepage():
    return render_template("home.html")


@app.route('/skills')
def skills():
    skills_content = Skill.query.all()
    return render_template("skills.html", skills=skills_content)


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
    posts = Post.query.all()
    return render_template("blog.html", posts=posts)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # Redirect to Admin after LogIn (Optional)
            return redirect(next_page) if next_page else redirect(url_for('homepage'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')  # (message, bootstrap class)

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog'))
    return render_template('new_post.html', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()  # No need to add since they are already in DB
        flash('Your post has been updated!', 'success')
        return redirect(url_for('blog', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new_post.html', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('blog'))


@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    users = User.query.all()
    form = UpdateAdminForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.skillName.data != "":
            skill = Skill(type='Soft', content=form.skillName.data)
            db.session.add(skill)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.skillName.data = ""

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('admin.html', image_file=image_file, form=form, users=users)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  # _ is a value that we don't need.
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)
    # Os is a module that have multiple methods to help us with files.
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename
