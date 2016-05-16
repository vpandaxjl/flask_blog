# -*- coding:utf-8 -*-
from app import db
from django.conf.urls import url
from unicodedata import category

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(65535), index=True)
    describe = db.Column(db.Text(65535), index=True)
    content = db.Column(db.Text(65535), index=True)
    author = db.Column(db.Text(65535), index=True)
    time = db.Column(db.String(80),index=True)
    category = db.Column(db.String(80), index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    

class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.String(64),  index=True)
    number = db.Column(db.Integer, index=True)
    article = db.relationship('Article', backref='categorys')


def change_admin_password(newpass):
    change_password = User.query.filter_by(username='vpanda').first()
    change_password.password = newpass
    db.session.add(change_password)
    db.session.commit()

def create_cate(new_cate):
    new_cate_to_data = Category(category=new_cate)
    db.session.add(new_cate_to_data)
    db.session.commit()

def category_data_add():
    for i in db.session.query(Category.category).all():
        cate_count = Article.query.filter_by(category = i[0]).count()
        cate_count_to_data = Category.query.filter_by(category=i[0]).first()
        cate_count_to_data.number = cate_count
        db.session.add(cate_count_to_data)
    db.session.commit()

def category_data():
    cate_date =  db.session.query(Category.category,Category.id,Category.number)
    return cate_date.all()

def article_id(cate_id):
    cate_all = db.session.query(Article.id,Article.title,Article.time,Article.category,Article.role_id).order_by(Article.id.desc())
    return cate_all.filter(Article.role_id == cate_id).all()

def article_all():
    cate_all = db.session.query(Article.id,Article.title,Article.time,Article.category,Article.role_id).order_by(Article.id.desc())
    return cate_all.all()
   
def delete_cate(del_id):
    del_data = Category.query.filter_by(id=del_id).first()
    del_data_in_other = Article.query.filter_by(role_id=del_id).first()
    if del_data_in_other == None:
        db.session.delete(del_data)
        db.session.commit()
        return True
    else:
        return False
        
def create_post(give_title, giv_des, give_content,author,give_time,give_select):
    cate_all = db.session.query(Category.id,Category.category)
    give_role_id = cate_all.filter(Category.category == give_select).first()[0]
    new_post_to_data = Article(title=give_title,
                               describe=giv_des,
                               content=give_content,
                               author=author,
                               time=give_time,
                               category=give_select,
                               role_id=give_role_id
                               )
    db.session.add(new_post_to_data)
    db.session.commit()

def delete_post(del_id):
    del_data = Article.query.filter_by(id=del_id).first()
    if del_data:
        db.session.delete(del_data)
        db.session.commit()
        return True
    else:
        return False