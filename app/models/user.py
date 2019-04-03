from app import db
from app import login
from hashlib import md5
from app.models import Post
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


followers = db.Table('followers',
  db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))    
)

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

class User(UserMixin, db.Model):
  __tablename__ = "user"

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  about_me = db.Column(db.String(140))
  last_seen = db.Column(db.DateTime, default=datetime.utcnow)
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  followed = db.relationship(
    'User', secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    backref=db.backref('followers', lazy='dynamic',), lazy='dynamic'
    )

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def avatar(self, size):
    digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    gravatar = 'https://www.gravatar.com/avatar/{}?d=robohash&s={}'.format(digest,size)
    return gravatar
  
  def is_following(self, other_user):
    return self.followed.filter(
      followers.c.followed_id == other_user.id).count() > 0

  def follow(self, other_user):
    if(not self.is_following(other_user)): self.followed.append(other_user)
  
  def unfollow(self, other_user):
    if(self.is_following(other_user)): self.followed.remove(other_user)
  
  def get_followed_posts(self):
    return Post.query.join(
      followers, (followers.c.followed_id == Post.user_id)).filter(
        followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

  def __repr__(self):
    return '<User {}>'.format(self.username)   

