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
        self.param = param
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
        return render_template('password_manage.html',state=True,form=form,params_dict=params_dict)
    def post_manage(self):
        #category_data = models.category_data()
        cate_all = models.article_all(self.param)
        return render_template('post_manage.html',state=True,params_dict=params_dict,cate_all=cate_all)
    def tag_manage(self):
        return render_template('tag_manage.html',state=True,params_dict=params_dict)

cate_dict={
           'create':'category_create',
           'delete':'category_delete'
           }
post_dict={
           'create':'post_create',
           'delete':'post_delete',
           'edit':'post_edit'
           }

def cate_url(name,param):
    if name == None:
        category_data = models.category_data()
        return render_template('category_manage.html',state=True,params_dict=params_dict,category_data=category_data)
    elif name.isdigit() and name not in cate_dict:
        cate_all = models.article_id(name,param)
        return render_template('article_manage.html',state=True,params_dict=params_dict,cate_all=cate_all,name=name)
    elif name in cate_dict:
        return eval(cate_dict[name])(param)
    else:
        return 'not found', 404
    
def cate_post_url(name,param,where,cate):
    if name in post_dict:
        return eval(post_dict[name])(param,where,cate)
    else:
        return 'not found', 404
    
def category_create(param=None):
    form = create_cate()
    if form.validate_on_submit():
        models.create_cate(form.name.data)
        flash('添加成功')
        return render_template('category_create.html',state=True,params_dict=params_dict,form=form)
    return render_template('category_create.html',state=True,params_dict=params_dict,form=form)

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
    return render_template('post_create.html',state=True,params_dict=params_dict,category_data=category_data,form=form)


class index_right():
    def __init__(self,state):
        self.cate_all = models.category_data()
        self.state = state
    def index(self,id):
        if id == None:
            id = 1
        else:
            id = int(id) 
        post_all = models.index_article_all(id)
        state = self.state
        return render_template('index.html',state=state,params_dict=params_dict,cate_all=self.cate_all,post_all=post_all)
    
def post_id(id,state):
    cate_all = models.category_data()
    post_content=models.post_content(id)
    return render_template('post.html',state=state,params_dict=params_dict,cate_all=cate_all,post_content=post_content)

def post_edit(param,where,cate):
    if param or request.method == 'POST':
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
                models.edit_post(give_title, giv_des, give_content,give_author,give_time,give_select,param)
                flash('修改成功')
                return redirect('/admin/post/edit/?id=%d' %int(param))
            else:
                flash('不能有空内容')
                return redirect('/admin/post/edit/?id=%d' %int(param))
        category_data = models.category_data()
        post_content=models.post_content(param)
        return render_template('post_edit.html',state=True,params_dict=params_dict,post_content=post_content,form=form,category_data=category_data)
    else:
        return 'not found', 404
    

def category_id(state,id,param):
    cate_all = models.category_data()
    post_content=models.article_category_all(id,int(param))
    return render_template('index_category.html',state=state,params_dict=params_dict,cate_all=cate_all,post_content=post_content,id=id)
    