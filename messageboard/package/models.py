"""
MODELS
"""


from datetime import datetime
from package import db, loginmanager
from flask_login import UserMixin

@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    profile_image = db.Column(db.String(200), unique=False, nullable=False, default="userimage.png")
    posts = db.relationship('Post', backref='author', lazy=True)


    def __repr__(self):
        return f"User('{self.username}', '{self.profile_image}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(40), nullable=False)
    content = db.Column(db.String(240), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)