from app import app
from app.forms import LoginForm
from app.models.user import User
from flask_login import current_user, login_user
from flask import render_template, flash, redirect, url_for


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

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if (current_user.is_authenticated): return redirect(url_for('index'))

    form = LoginForm()

    if (form.validate_on_submit()):

        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data
        user = User.query.filter_by(username=username).first()

        if (user is None or not user.check_password(password)):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            login_user(user, remember=remember)
            return redirect(url_for('index'))
            
    return render_template('login.html', title='Sign In', form=form)
