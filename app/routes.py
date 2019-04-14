from app import db
from app import app
from flask import request
from datetime import datetime
from app.forms import LoginForm
from app.models.user import User
from app.models.post import Post
from werkzeug.urls import url_parse
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user, login_user
from flask import render_template, flash, redirect, url_for
from app.forms import EditProfileForm, RegistrationForm, PostForm

@app.before_request
def before_rquest():
    if (current_user.is_authenticated):
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()

    if( form.validate_on_submit()):
        body = form.post.data
        post = Post(body=body, author=current_user)

        db.session.add(post)
        db.session.commit()

        flash('Your post is now online')
        return redirect(url_for('index'))

    page = request.args.get('page',1, type=int)
    posts = current_user.get_followed_posts().paginate(
        page, app.config["POSTS_PER_PAGE"], False)
    
    if (posts.has_next): next_url = url_for('index', page=posts.next_num)
    else: next_url = None
    
    if (posts.has_prev): prev_url = url_for('index', page=posts.prev_num)
    else: prev_url = None

    return render_template(
        'index.html', title='Home Page', posts=posts.items, 
        form=form, next_url=next_url, prev_url=prev_url)

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

            if(not next_page or url_parse(next_page).netloc != ''): next_page = url_for('index')
            return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if (current_user.is_authenticated): return redirect(url_for('index'))
    
    form = RegistrationForm()

    if(form.validate_on_submit()):

        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now are register user!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title="Register", form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    if (posts.has_next): next_url = url_for('user', username=user.username ,page=posts.next_num)
    else: next_url = None
    
    if (posts.has_prev): prev_url = url_for('user',  username=user.username, page=posts.prev_num)
    else: prev_url = None    


    return render_template(
        'user.html', title='profile',user=user, posts=posts.items,
        next_url=next_url, prev_url=prev_url
        )

@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    
    form = EditProfileForm(current_user.username)

    if( request.method == 'GET'):

        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    elif (form.validate_on_submit()):

        new_username = form.username.data
        new_about_me = form.about_me.data
        current_user.username = new_username
        current_user.about_me = new_about_me
        db.session.commit()

        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    
    return render_template('edit_profile.html', title='Edit profile', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()

    if (user is None): 
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))

    elif (username == current_user):
        flash('You cannot follow yourself!')
        return redirect(url_for('index'))
    else:
        current_user.follow(user)
        db.session.commit()

        flash('You are following {}'.format(username))
        return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()

    if(user is None):
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    
    elif(user == current_user):
        flash('You were not even following yourself!')
        return redirect(url_for('user', username=username))
    else:
        current_user.unfollow(user)
        db.session.commit()

        flash('You are not following {}'.format(username))
        return redirect(url_for('user', username=username))

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page',1,type=int)
    all_posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    
    if (all_posts.has_next): next_url = url_for('explore', page=all_posts.next_num)
    else: next_url = None
    
    if (all_posts.has_prev): prev_url = url_for('explore', page=all_posts.prev_num)
    else: prev_url = None

    return render_template(
        'index.html', title="Explore", posts=all_posts.items,
        next_url=next_url, prev_url=prev_url
        )