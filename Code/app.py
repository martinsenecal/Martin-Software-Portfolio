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



if __name__ == '__main__':
    app.run()
