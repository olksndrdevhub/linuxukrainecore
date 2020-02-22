from app import db
from datetime import datetime
import re

from flask_security import UserMixin, RoleMixin

def slugefy(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)

post_tags = db.Table('post_tags',
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
    )

user_posts = db.Table('user_posts',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
    )



class Post(db.Model):

    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.String)
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime)
    img_filename = db.Column(db.String)
    author = db.Column(db.String(20))
    
    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()
        self.set_create_time()

    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))
    # author = db.relationship('User', secondary=user_posts, backref=db.backref('posts', lazy='dynamic'))

    def generate_slug(self):
        if self.title:
            self.slug = slugefy(self.title)

    def set_create_time(self):
        if self.title:
            self.created = datetime.now()

    def __repr__(self):
        return '<Post id: {}, title: {}, slug: {}>'.format(self.id, self.title, self.slug)

    def set_author(self, current_user):
        if self.title:
            self.author = str(current_user)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugefy(self.name)

    
    def generate_slug(self):
        if self.name:
            self.slug = slugefy(self.name)

    def __repr__(self):
        return '{}'.format(self.name)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_filename = db.Column(db.String)
    

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    )





class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(40))
    secname = db.Column(db.String(40))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    slug = db.Column(db.String(100))
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.slug = slugefy(self.login)

    def generate_slug(self):
        if self.login:
            self.slug = slugefy(self.login)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))