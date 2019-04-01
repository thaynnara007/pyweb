from app import app
from flask import request
from app.forms import LoginForm
from app.models.user import User
from werkzeug.urls import url_parse
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user, login_user
from flask import render_template, flash, redirect, url_for


@app.route('/')
@app.route('/index')
@login_required
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
            next_page = request.args.get('next')

            if (next_page or url_parse(next_page).netloc == ''): next_page = url_for('index')
            return redirect(url_for(next_page))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))