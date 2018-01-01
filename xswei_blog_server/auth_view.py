from xswei_blog_server import app
import os, json, datetime
from flask import url_for,request,redirect,render_template,abort,flash
from flask.ext.login import (LoginManager, login_required,
                               login_user, logout_user,UserMixin)
from xswei_blog_server.utils import (legal_path,parse_path,del_item,
                                     add_item, full_path)
import pickle

# login settings=========================

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_message="请登录"
login_manager.login_message_category = "info"
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False

@login_manager.user_loader
def load_user(user_id):

    #user = User(222)
    #return user
    if user_id == '1':
        with open('xswei_blog_server/root_user.pickle', 'rb') as f:
            user = pickle.load(f)
        return user
    else:
        return None
    #TODO: user!!!!!

    
# view functions=============================
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form['uname']=='root' and request.form['password']=='aptx4869':
            remember = True if 'remember' in request.form else False
            with open('xswei_blog_server/root_user.pickle', 'rb') as f:
                _root_user = pickle.load(f)
            login_user(_root_user,remember=remember)
            flash('登录成功!')
            return redirect(url_for("list_blog"))
        flash('登陆失败!检查用户名和密码.')
        return render_template("login.html",title='login')
    return render_template("login.html",title='login')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route("/new")
@login_required
def new():
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    return render_template("editormd.html", date=date)

@app.route("/edit/<md_type>/<path:fpath>")
@login_required
def edit(fpath, md_type):
    fpath = legal_path(fpath, md_type)
    if not fpath:
        abort(404)
    y, m, d, title = parse_path(fpath, md_type)
    date = "{}-{}-{}".format(y, m, d)
    return render_template("editormd.html",md_path=fpath, date=date, title=title, md_type=md_type)

@app.route("/delete_draft/<path:fpath>")
@login_required
def delete_draft(fpath):
    fpath = legal_path(fpath, md_type='draft')
    if not fpath:
        abort(404)
    try:
        full_fpath = full_path(fpath, 'draft', app.config)
        os.remove(full_fpath+'.md')
        del_item(app.config['DRAFTS_INDEX'], fpath)
        flash('已删除')
    except Exception as e:
        flash('删除失败！请重试')
        return redirect(url_for("list_drafts"))
    return redirect(url_for("list_drafts"))

@app.route("/publish",methods=['POST'])
@login_required
def publish():
    date = request.form['date']
    title = request.form.get('title','untitled')
    if title=='':
        title='untitled'
    y,m,d = date.split('-')[0:3]
    fpath = legal_path('{}/{}/{}/{}'.format(y, m, d, title), md_type='blog')
    if not fpath:
        abort(404)
    save_dir = 'data_dir/published/{}/{}/{}'.format(y,m,d)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    full_path = os.path.join('data_dir/published',fpath)
    md_name = full_path + '.md'
    draft_path = legal_path('{}-{}-{}-{}'.format(y,m,d,title), md_type='draft')
    md = request.form['md']
    try:
        with open(md_name,'w',encoding='utf-8') as mdf:
            mdf.write(md)
        add_item('data_dir/published/index.json', fpath)
        full_draft_path = 'data_dir/drafts/{}.md'.format(draft_path)
        if os.path.exists(full_draft_path):
            os.remove(full_draft_path)
        del_item('data_dir/drafts/index.json', draft_path)
        flash('发表成功！')
    except:
        flash('发表失败！')
        return url_for("list_blog")
    return url_for("list_blog")

@app.route("/delete_blog/<path:save_name>")
@login_required
def delete_blog(save_name):
    save_name = legal_path(save_name, md_type='blog')
    if not save_name:
        abort(404)
    save_dir,title = os.path.split(save_name)
    save_dir = os.path.join('data_dir/published',save_dir)
    try:
        os.remove(os.path.join(save_dir,title+'.md'))
        del_item('data_dir/published/index.json', save_name)
        flist = os.listdir(save_dir)
        flash('删除成功！')
        for f in flist:
            if os.path.splitext(f)[1] == '.md':
                return redirect(url_for("list_blog"))
        os.removedirs(save_dir)
    except:
        flash('删除失败！')
        return redirect(url_for("list_blog"))
    return redirect(url_for("list_blog"))

@app.route("/save_draft", methods=['POST'])
@login_required
def save():
    date = request.form['date']
    title = request.form.get('title', 'untitled')
    if title=='':
        title='untitled'
    save_name= '{}-{}'.format(date,title)
    save_name = legal_path(save_name, md_type='draft')
    if not save_name:
        abort(404)
    md = request.form['md']
    save_dir = 'data_dir/drafts'
    full_save_name = '{}/{}.md'.format(save_dir,save_name)
    try:
        with open(full_save_name, 'w',encoding='utf-8') as mdf:
            mdf.write(md)
        add_item('data_dir/drafts/index.json', save_name)
    except:
        return '保存失败!'
    return '保存成功！'