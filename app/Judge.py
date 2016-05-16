# -*- coding:utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy
import models,datetime
from flask import session,redirect,render_template,url_for,flash,request
from Form_table import change_admin_password,create_cate,create_post
from params import params_dict



class user():
    def __init__(self,user,passwd):
        self.username = user
        self.password = passwd
        self.__db_username = models.User.query.filter_by(username = user).first()
        self.__db_password = models.User.query.filter_by(password = passwd).first()
    def judge_user(self):
        if self.__db_username and self.__db_password:
            session['username'] = self.username
            return redirect('/admin/')
        else:
            flash('你输入的账号或密码有误！请重新输入')
            return redirect('/login/')
        
        
class admin_url():
    def __init__(self,url,param):
        self.url = url
        self.url_dict = {
             'post':'post_manage',
                'tag':'tag_manage',
        'password':'password_manage'     
                         }
        
    def url_judge(self):
        if self.url in self.url_dict:
            return eval('self.'+(self.url_dict)[self.url])()
        else:
            return 'not found', 404
    def password_manage(self):
        form = change_admin_password()
        if form.validate_on_submit():
            models.change_admin_password(form.passwd.data)
            flash('修改成功')
            return redirect('/admin/password/')
        return render_template('password_manage.html',form=form,params_dict=params_dict)
    def post_manage(self):
        category_data = models.category_data()
        cate_all = models.article_all()
        return render_template('post_manage.html',params_dict=params_dict,cate_all=cate_all)
    def tag_manage(self):
        return render_template('tag_manage.html',params_dict=params_dict)

cate_dict={
           'create':'category_create',
           'delete':'category_delete'
           }
post_dict={
           'create':'post_create',
           'delete':'post_delete'
           }

def cate_url(name,param):
    if name == None:
        category_data = models.category_data()
        return render_template('category_manage.html',params_dict=params_dict,category_data=category_data)
    elif name.isdigit() and name not in cate_dict:
        cate_all = models.article_id(name)
        return render_template('article_manage.html',params_dict=params_dict,cate_all=cate_all)
    elif name in cate_dict:
        return eval(cate_dict[name])(param)
    else:
        return 'not found', 404
    
def cate_post_url(name,param,where,cate):
    if name in cate_dict:
        return eval(post_dict[name])(param,where,cate)
    else:
        return 'not found', 404
    
def category_create(param=None):
    form = create_cate()
    if form.validate_on_submit():
        models.create_cate(form.name.data)
        flash('添加成功')
        return render_template('category_create.html',params_dict=params_dict,form=form)
    return render_template('category_create.html',params_dict=params_dict,form=form)

def category_delete(param):
    if param == None:
        return 'not found', 404
    else:
        del_res = models.delete_cate(param)
        if del_res == True:
            return redirect('/admin/category/')
        else:
            flash('该分类不为空')
            return redirect('/admin/category/')

def post_delete(param,where,cate):
    del_res = models.delete_post(param)
    if del_res == True:
        if where == 'post':
            models.category_data_add()
            return redirect('/admin/post/')
        elif where == 'article':
            models.category_data_add()
            return redirect('/admin/category/%s'  %cate)
    else:
        return 'not found', 404
    
def post_create(param,where,cate):
    category_data = models.category_data()
    form = create_post()
    if form.validate_on_submit():
        give_title = request.form['title']
        giv_des = request.form['post_des']
        give_select = request.form['select']
        give_content = request.form['editor1']
        now = datetime.datetime.now()
        give_time = now.strftime('%Y-%m-%d %H:%M:%S')
        give_author = 'Vpanda'
        if give_content != '' and give_title != '' and giv_des != '':
            models.create_post(give_title, giv_des, give_content,give_author,give_time,give_select)
            models.category_data_add()
            return redirect('/admin/post/')
        else:
            flash('不能有空内容')
            return redirect('/admin/post/create/')
    return render_template('post_create.html',params_dict=params_dict,category_data=category_data,form=form)

class index_right():
    def __init__(self):
        self.cate_all = models.category_data()
    def index(self):
        return render_template('index.html',cate_all=self.cate_all,params_dict=params_dict)