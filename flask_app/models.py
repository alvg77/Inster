from datetime import datetime
from flask_app import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as sl
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Chat = db.Table('Chat',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('room_id', db.Integer, db.ForeignKey('room.id')),
# )

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    posts = db.relationship('Posts', backref='author', lazy=True)
    comments = db.relationship('Comments', backref='author', lazy=True)
    liked = db.relationship('Likes', foreign_keys='Likes.user_id', backref='user', lazy='dynamic')
    followed = db.relationship('User', secondary=followers, primaryjoin=(followers.c.follower_id == id), secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
    def get_reset_token(self, expires_sec=1800):
        s = sl(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = sl(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    def followed_posts(self):
        return Posts.query.join(
            followers, (followers.c.followed_id == Posts.user_id)).filter(
                followers.c.follower_id == self.id).order_by(Posts.date_posted.desc())
    
    def like_post(self, post):
        if not self.is_liked(post):
            like = Likes(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.is_liked(post):
            Likes.query.filter_by(user_id=self.id, post_id=post.id).delete() 
    
    def is_liked(self, post):
        return Likes.query.filter(Likes.user_id == self.id, Likes.post_id == post.id).count() > 0
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_image}')"

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    post_image = db.Column(db.String(20), nullable=True)
    comments = db.relationship('Comments', backref='post', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('Likes', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    
    def __repr__(self):
        return f"Comment('{self.id}', '{self.user_id}')"
    
class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

# class Messages(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     message = db.Column(db.String(500), nullable=True)
#     room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    
# class Room(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     messages = db.relationship('Messages', backref='messages', lazy=True)
#     users = db.relationship('User', secondary=Chat, backref='user_rooms')

#     def add_user(self, user):
#         if not self.in_room(user):
#             self.users.append(user)
    
#     def in_room(self, user):
#         for i in self.users:
#             if i == user:
#                 return True
#         return False