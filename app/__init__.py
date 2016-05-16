# -*- coding:utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__) 
app.config.from_object('config') 

db = SQLAlchemy(app,use_native_unicode="utf8")  ##解决数据库编码问题


from app import views,models

#db.create_engine  ##初始化
#db.create_all()   ##创建表，如果存在则不创建
