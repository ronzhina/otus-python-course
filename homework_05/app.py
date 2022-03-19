from flask import Flask, render_template

app = Flask(__name__)


@app.get('/')
def index():
    return render_template(
        'base.html',
        body_text="<q>Be yourself; everyone else is already taken.</q> – Oscar Wilde")


@app.get('/about/')
def about():
    return render_template(
        'base.html',
        body_text="This is my first app with Flask :)")
