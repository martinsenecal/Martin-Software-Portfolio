from flask import Flask, url_for, render_template

app = Flask(__name__)


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


@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")


if __name__ == '__main__':
    app.run()
