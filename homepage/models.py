from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from homepage import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    date_joined = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    password = db.Column(db.String(60), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')
    posts = db.relationship('Post', backref='author', lazy=True)
    comments_ = db.relationship('Comment', backref='author_comment', lazy=True)
    newsletter = db.Column(db.Boolean(), nullable=False, default = False)
    activated = db.Column(db.Boolean(), nullable=False, default = False)

    


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.image_file}', '{self.roles}' )"


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    abstract = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comment', backref='post_comment', lazy=True)
    who_liked = db.relationship('User', backref='post_liked', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}' )"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pid = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    def __repr__(self):
        return f"Comment('{self.id}', '{self.content}')"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False, unique=True)

    def __repr__(self):
        return f"Role('{self.id}', '{self.name}' )"

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
    
    def __repr__(self):
        return f"Role('{self.user_id}', '{self.role_id}' )"

class PostLikes(db.Model):
    __tablename__ = 'post_likes'
    id = db.Column(db.Integer(), primary_key=True)#
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"Role('{self.user_id}', '{self.post_id}' )"

class CommentLikes(db.Model):
    __tablename__ = 'comment_likes'
    id = db.Column(db.Integer(), primary_key=True)#
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    comment_id = db.Column(db.Integer(), db.ForeignKey('comments.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"Role('{self.user_id}', '{self.comment_id}' )"