# -*- coding:utf-8 -*-
SECRET_KEY = 'this is key xxx'

SQLALCHEMY_DATABASE_URI='mysql://root@127.0.0.1/blog' ##mysql
#SQLALCHEMY_DATABASE_URI='sqlite:///datadb.db'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS  = True
