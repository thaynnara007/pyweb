from flask import render_template
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {"username" : "Vin", "power" : "Mistborn"}
    posts = [
        {
            'author':{"username":"Kelsier"},
            'body': "Let's defeat the Lord Ruler!",
        },
        {
            'author':{'username':'Elend'},
            'body': 'Lets resolve this with a discussion'
        }
    ]

    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
