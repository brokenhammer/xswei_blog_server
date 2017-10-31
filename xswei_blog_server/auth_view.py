from xswei_blog_server import app
import os, json, datetime
from flask import url_for,request,redirect,render_template,abort
from flask.ext.login import (LoginManager, login_required,
                               login_user, logout_user,UserMixin)

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
#=========================================
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        print(request.form)
        if request.form['uname']=='root' and request.form['password']=='aptx4869':
            user=User()
            login_user(user)
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

@app.route("/edit/<path:fpath>")
@login_required
def edit(fpath):
    if '/' in fpath:
        y,m,d,title = fpath.split('/')
    else:
        y,m,d,title = fpath.split('-')
    date = "{}-{}-{}".format(y,m,d)
    return render_template("editormd.html",md_path=fpath, date=date,title=title)

@app.route("/delete_drafts/<path:save_name>")
@login_required
def delete_drafts(save_name):
    if '..' in save_name:
        abort(404)
    save_name+='.md'
    os.remove(os.path.join('data_dir/drafts',save_name))
    return redirect(url_for("list_drafts"))

@app.route("/publish",methods=['POST'])
@login_required
def publish():
    date = request.form['date']
    title = request.form.get('title','untitled')
    if title=='':
        title='untitled'
    y,m,d = date.split('-')
    md = request.form['md']
    save_dir = 'data_dir/published/{}/{}/{}'.format(y,m,d)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    publish_name = os.path.join(save_dir,title)
    md_name = publish_name + '.md'
    with open(md_name,'w',encoding='utf-8') as mdf:
        mdf.write(md)
    draft_form = 'data_dir/drafts/{}-{}-{}-{}.md'.format(y,m,d,title)
    if os.path.exists(draft_form):
        os.remove(draft_form)
    return url_for("list_blog")

@app.route("/delete_blog/<path:save_name>")
@login_required
def delete_blog(save_name):
    save_dir,title = os.path.split(save_name)
    save_dir = os.path.join('data_dir/published',save_dir)
    os.remove(os.path.join(save_dir,title+'.md'))
    flist = os.listdir(save_dir)
    for f in flist:
        if os.path.splitext(f)[1] == '.md':
            return redirect(url_for("list_blog"))
    os.removedirs(save_dir)
    return redirect(url_for("list_blog"))

@app.route("/save_draft", methods=['POST'])
@login_required
def save():
    date = request.form['date']
    title = request.form.get('title', 'untitled')
    if title=='':
        title='untitled'
    save_name= '{}-{}.md'.format(date,title)
    md = request.form['md']
    save_dir = 'data_dir/drafts'
    with open(os.path.join(save_dir,save_name), 'w',encoding='utf-8') as mdf:
        mdf.write(md)
    return '保存成功！'