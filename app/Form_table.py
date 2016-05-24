# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired
from wtforms.fields.simple import PasswordField
from wtforms.fields.core import BooleanField

class login_admin(Form):
    name = StringField('name', validators=[DataRequired()])
    passwd = PasswordField('password', validators=[DataRequired()])

class change_admin_password(Form):
    passwd = PasswordField('password', validators=[DataRequired()])
    
class create_cate(Form):
    name = StringField('name', validators=[DataRequired()])
    
class create_post(Form):
    recommend = BooleanField('recommend')
    pass
    