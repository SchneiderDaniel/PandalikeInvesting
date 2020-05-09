from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from homepage import db, login_manager
from flask_login import UserMixin
from homepage.search import add_to_index, remove_from_index, query_index

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


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
    portfolios = db.relationship('Portfolio', backref='creator', lazy=True)
    comments_ = db.relationship('Comment', backref='author_comment', lazy=True)
    discussions_ = db.relationship('Discussion', backref='author_discussion', lazy=True)
    newsletter = db.Column(db.Boolean(), nullable=False, default = False)
    activated = db.Column(db.Boolean(), nullable=False, default = False)
    banned = db.Column(db.Boolean(), nullable=False, default = False)

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


class Post(SearchableMixin, db.Model):
    __tablename__ = 'posts'
    __searchable__ = ['content']
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
    discussions = db.relationship('Discussion', backref='comment_discussion', lazy=True)
    reports = db.relationship('Report', backref='comment_report', lazy=True)
    def __repr__(self):
        return f"Comment('{self.id}', '{self.content}')"


class Discussion(db.Model):
    __tablename__ = 'discussions'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    def __repr__(self):
        return f"Discussion('{self.id}', '{self.content}')"

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    complain = db.Column(db.Text, nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    def __repr__(self):
        return f"Report('{self.id}', '{self.complain}')"


class Newsletter(db.Model):
    __tablename__ = 'newsletters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    sendOut = db.Column(db.Boolean(), nullable=False, default = False)
   
    def __repr__(self):
        return f"Comment('{self.id}')"

class Tag(db.Model):
    __tablename__ = 'theTags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    def __repr__(self):
        return f"Role('{self.id}', '{self.name}' )"

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
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"Role('{self.user_id}', '{self.post_id}' )"

class PostTags(db.Model):
    __tablename__ = 'post_tags'
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id', ondelete='CASCADE'))
    tag_id = db.Column(db.Integer(), db.ForeignKey('theTags.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"Role('{self.user_id}', '{self.post_id}' )"

class CommentLikes(db.Model):
    __tablename__ = 'comment_likes'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    comment_id = db.Column(db.Integer(), db.ForeignKey('comments.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"Role('{self.user_id}', '{self.comment_id}' )"



class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text, nullable=False)
    numberPositions = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    positions = db.relationship('Position', backref='portfolio', lazy=True)
    def __repr__(self):
        return f"Portfolio('{self.name}', Size: '{self.numberPositions}')"
    
    @staticmethod
    def hasOneCurrency(pf):

        currency = ""

        for pos in pf.positions:
            if  currency=="":
                currency = pos.currency
            else:
                if pos.currency!=currency:
                    return False
                
        return True
            

        

class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, default = "Empty")
    ticker = db.Column(db.Text, nullable=False, default = "Empty")
    percent =  db.Column(db.Float, nullable=False, default = "0.0")
    currency = db.Column(db.Text,nullable=False, default = 'NA')
    port_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable= False)
    
   
    def __repr__(self):
        return f"Position('{self.name}', Size: '{self.percent}')"
