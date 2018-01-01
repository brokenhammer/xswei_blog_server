from blog_server import app
import os, json, datetime
from flask import url_for,request,redirect,render_template,abort,flash
from flask.ext.login import (LoginManager, login_required,
                               login_user, logout_user,UserMixin)
from blog_server.utils import (legal_path, parse_path, del_item,
                               add_item, full_path, construct_fpath)
import pickle

# login settings=========================

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_message="请登录"
login_manager.login_message_category = "info"
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    if user_id == '1':
        with open('blog_server/root_user.pickle', 'rb') as f:
            user = pickle.load(f)
        return user
    else:
        return None
    
# view functions=============================
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form['uname']=='root' and request.form['password']=='aptx4869':
            remember = True if 'remember' in request.form else False
            with open(app.config['ROOT_FILE'], 'rb') as f:
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
    fpath = construct_fpath(title, y, m, d, md_type='blog')
    if not fpath:
        abort(404)
    full_fpath = full_path(fpath,'blog',app.config)
    save_dir = os.path.dirname(full_fpath)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    draft_path = construct_fpath(title, y, m, d, md_type='draft')
    md = request.form['md']
    try:
        with open(full_fpath + '.md', 'w', encoding='utf-8') as mdf:
            mdf.write(md)
        add_item(app.config['BLOGS_INDEX'], fpath)
        full_draft_path = full_path(draft_path, 'draft', app.config)
        print(full_draft_path)
        if os.path.exists(full_draft_path + '.md'):
            os.remove(full_draft_path + '.md')
        del_item(app.config['DRAFTS_INDEX'], draft_path)
        flash('发表成功！')
    except:
        flash('发表失败！')
        return url_for("list_blog")
    return url_for("list_blog")

@app.route("/delete_blog/<path:fpath>")
@login_required
def delete_blog(fpath):
    fpath = legal_path(fpath, md_type='blog')
    if not fpath:
        abort(404)
    full_fpath = full_path(fpath, 'blog', app.config)
    save_dir,title = os.path.split(full_fpath)
    try:
        os.remove(full_fpath + '.md')
        del_item(app.config['BLOGS_INDEX'], fpath)
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
    fpath = legal_path('{}-{}'.format(date,title), md_type='draft')
    if not fpath:
        abort(404)
    md = request.form['md']
    full_fpath = full_path(fpath, 'draft', app.config)
    try:
        with open(full_fpath + '.md', 'w',encoding='utf-8') as mdf:
            mdf.write(md)
        add_item(app.config['DRAFTS_INDEX'], fpath)
    except:
        return '保存失败!'
    return '保存成功！'