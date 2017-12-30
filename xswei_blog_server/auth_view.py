from xswei_blog_server import app
import os, json, datetime
from flask import url_for,request,redirect,render_template,abort,flash
from flask.ext.login import (LoginManager, login_required,
                               login_user, logout_user,UserMixin)
from xswei_blog_server.utils import legal_path,parse_path

# login settings=========================
app.secret_key = '2A3dd9df.}-'
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_message="请登录"
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin):
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return "1"

@login_manager.user_loader
def load_user(user_id):
    user=User()
    return user

# view functions=============================
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        print(request.form)
        if request.form['uname']=='root' and request.form['password']=='aptx4869':
            _user=User()
            login_user(_user)
            #TODO: Remember me
            return redirect(url_for("list_blog"))
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

@app.route("/delete_drafts/<path:save_name>")
@login_required
def delete_drafts(save_name):
    #TODO:JSON file
    save_name = legal_path(save_name, md_type='draft')
    if not save_name:
        abort(404)
    save_name += '.md'
    try:
        os.remove(os.path.join('data_dir/drafts',save_name))
        flash('已删除')
    except Exception as e:
        flash('删除失败！请重试')
        #TODO:LOGGING
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
    legal_draft_path = legal_path('{}-{}-{}-{}'.format(y,m,d,title), md_type='draft')
    draft_form = 'data_dir/drafts/{}.md'.format(legal_draft_path)
    md = request.form['md']
    try:
        with open(md_name,'w',encoding='utf-8') as mdf:
            mdf.write(md)
        if os.path.exists(draft_form):
            os.remove(draft_form)
        flash('发表成功！')
    except:
        flash('发表失败！')
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
        flist = os.listdir(save_dir)
        for f in flist:
            if os.path.splitext(f)[1] == '.md':
                return redirect(url_for("list_blog"))
        os.removedirs(save_dir)
        flash('删除成功！')
    except:
        flash('删除失败！')
    return redirect(url_for("list_blog"))

@app.route("/save_draft", methods=['POST'])
@login_required
def save():
    date = request.form['date']
    title = request.form.get('title', 'untitled')
    if title=='':
        title='untitled'
    save_name= '{}-{}.md'.format(date,title)
    save_name = legal_path(save_name, md_type='draft')
    if not save_name:
        abort(404)
    md = request.form['md']
    save_dir = 'data_dir/drafts'
    with open(os.path.join(save_dir,save_name), 'w',encoding='utf-8') as mdf:
        mdf.write(md)
    return '保存成功！'