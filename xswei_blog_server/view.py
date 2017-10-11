from xswei_blog_server import app
from flask import render_template,request,redirect,url_for,abort
import os,datetime
import urllib.parse
@app.route("/")
def root():
    return redirect(url_for('login'))

@app.route("/login/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        return redirect(url_for("list_blog"))
    return render_template("login.html", title="login")

@app.route("/new")
def new():
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    return render_template("editormd.html", date=date)

@app.route("/edit/<path:fpath>")
def edit(fpath):
    if '/' in fpath:
        y,m,d,title = fpath.split('/')
    else:
        y,m,d,title = fpath.split('-')
    date = "{}-{}-{}".format(y,m,d)
    return render_template("editormd.html",md_path=fpath, date=date,title=title)

@app.route("/load_blog_md/<path:fpath>")
def data_request(fpath):
    fpath = urllib.parse.unquote(fpath)
    if '-' in fpath: # drafts
        save_dir = 'data_dir/drafts/'
    else: # published
        save_dir = 'data_dir/published/'
    save_name = save_dir + fpath + '.md'
    with open(save_name,'r',encoding='utf-8') as f:
        return f.read()

@app.route("/save_draft", methods=['POST'])
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

@app.route("/list_drafts")
def list_drafts():
    return render_template('list_drafts.html')

@app.route("/delete_drafts/<path:save_name>")
def delete_drafts(save_name):
    if '..' in save_name:
        abort(404)
    save_name+='.md'
    os.remove(os.path.join('data_dir/drafts',save_name))
    return redirect(url_for("list_drafts"))

@app.route("/publish",methods=['POST'])
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

@app.route("/list_blog")
def list_blog():
    return render_template('list_blog.html')

@app.route("/blog_view/<path:save_name>")
def blog_view(save_name):
    return render_template('blog_view.html',blog_path=save_name)

@app.route("/delete_blog/<path:save_name>")
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