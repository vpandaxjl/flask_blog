# -*- coding:utf-8 -*-
from app import app
from flask import render_template,redirect,session,request,url_for,make_response
from Form_table import login_admin
import Judge
from params import params_dict
import os,datetime,random



@app.route('/login/', methods=('GET', 'POST'))
def login():
    form = login_admin()
    state = 'username' in session
    if state:
        return redirect('/admin/')
    if form.validate_on_submit():   ##提交内容不为空则就是True
        user_judge = Judge.user(form.name.data,form.passwd.data)  ##得到表单数据
        return user_judge.judge_user()
    else:
        return render_template('login.html',form=form,state=state,params_dict=params_dict)


@app.route('/admin/')
@app.route('/admin/<url>/', methods=('GET', 'POST'))
def admin_manage(url=None):
    state = 'username' in session
    if request.args.get('id'):param = int(request.args.get('id'))
    else:param=1
    if url == None:
        if state:
            return render_template('admin.html',params_dict=params_dict,state=state)
        return redirect('/login/')
    elif state:
        url_judge = Judge.admin_url(url,param)
        return url_judge.url_judge()
    return redirect('/login/')

@app.route('/admin/category/')
@app.route('/admin/category/<name>/', methods=('GET', 'POST'))
@app.route('/admin/category/<name>/<cate_id>/', methods=('GET', 'POST'))
def category(name=None,cate_id=None):
    state = 'username' in session
    if request.args.get('id'):param = int(request.args.get('id'))
    else:param=1
    if state:
        return Judge.cate_url(name,cate_id,param)
    else:
        return redirect('/login/')
    

@app.route('/admin/post/<name>/', methods=('GET', 'POST'))
def admin_post(name=None):
    state = 'username' in session
    param = request.args.get('id')
    where = request.args.get('where')
    cate = request.args.get('cate')
    if state:
        return Judge.cate_post_url(name,param,where,cate)
    else:
        return redirect('/login/')

@app.route('/post/<int:id>/')
def post(id):
    state = 'username' in session
    return Judge.post_id(id,state)

@app.route('/category/<int:id>/')
def index_category(id):
    state = 'username' in session
    param = request.args.get('page')
    if param == None:param=1
    return Judge.category_id(state,id,param)

@app.route('/')
def index():
    state = 'username' in session
    id = request.args.get('id')
    index_right = Judge.index_right(state)
    return index_right.index(id)
    
@app.route('/logout/')
def logout():
    session.pop('username')
    return redirect('/login/')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html',params_dict=params_dict),404


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))

@app.route('/ckupload/', methods=['POST'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(app.static_folder, 'upload', rnd_name)
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'
    res = """

<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>

""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response
