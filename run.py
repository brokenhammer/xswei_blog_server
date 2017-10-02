#/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask,render_template,\
    request,redirect,url_for,abort
import os,datetime,uuid,json,codecs
import urllib.parse

app = Flask(__name__)
app.debug= True
@app.route("/")
def root():
    return redirect(url_for('login'))
    #return ("<h1>Hello from flask!</h1>")

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
    print(md.split('\n'))
    save_dir = 'data_dir/drafts'
    with open(os.path.join(save_dir,save_name), 'w',encoding='utf-8') as mdf:
        mdf.write(md)
    return '保存成功！'

@app.route("/list_drafts")
def list_drafts():
    file_list = os.listdir('data_dir/drafts')
    ret_dict = []
    for save_name in file_list:
        save_name = os.path.splitext(save_name)[0]
        ret_dict.append({'link':save_name, 'title':save_name.split('-')[-1],'date':save_name.split('-')[0:3]})
    return render_template('list_drafts.html',link2title=ret_dict)

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
    html = request.form['html']
    save_dir = 'data_dir/published/{}/{}/{}'.format(y,m,d)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    publish_name = os.path.join(save_dir,title)
    md_name = publish_name + '.md'
    html_name = publish_name + '.html'
    print(md.split('\n'))
    with open(md_name,'w',encoding='utf-8') as mdf:
        mdf.write(md)
    # with open(html_name, 'w',encoding='utf-8') as htmlf:
    #     htmlf.write(html)
    draft_form = 'data_dir/drafts/{}-{}-{}-{}.md'.format(y,m,d,title)
    if os.path.exists(draft_form):
        os.remove(draft_form)
    return url_for("list_blog")

@app.route("/list_blog")
def list_blog():
    years = os.listdir('data_dir/published')
    blog_set = []
    for y in years:
        months = os.listdir('data_dir/published/{}'.format(y))
        for m in months:
            days = os.listdir('data_dir/published/{}/{}'.format(y,m))
            for d in days:
                flist = os.listdir('data_dir/published/{}/{}/{}'.format(y,m,d))
                for f in flist:
                    if os.path.splitext(f)[1] == '.md':
                        title = os.path.splitext(f)[0]
                        blog_set.append('{}/{}/{}/{}'.format(y,m,d,title))
    blog_set.sort(reverse=True)
    ret_dict = []
    for blog in blog_set:
        title = blog.split('/')[-1]
        ret_dict.append({'link':blog,'title':title,'date':blog.split('/')[0:3]})
    return render_template('list_blog.html',link2title=ret_dict)

@app.route("/blog_view/<path:save_name>")
def blog_view(save_name):
    return render_template('blog_view.html',blog_path=save_name)
# @app.route('/get_blog_html/<path:save_name>')
# def get_blog_html(save_name):
#     save_name = 'data_dir/published/' + save_name + '.html'
#     save_dir, fname = os.path.split(save_name)
#     with open(save_name,encoding='utf-8') as f:
#         return f.read()

@app.route("/delete_blog/<path:save_name>")
def delete_blog(save_name):
    save_dir,title = os.path.split(save_name)
    save_dir = os.path.join('data_dir/published',save_dir)
    os.remove(os.path.join(save_dir,title+'.md'))
    os.remove(os.path.join(save_dir,title+'.html'))
    flist = os.listdir(save_dir)
    for f in flist:
        if os.path.splitext(f)[1] == '.md':
            return redirect(url_for("list_blog"))
    os.removedirs(save_dir)
    return redirect(url_for("list_blog"))

if __name__ =="__main__":
    if not os.path.exists('./data_dir/drafts'):
        os.makedirs('./data_dir/drafts')
    if not os.path.exists('./data_dir/published'):
        os.makedirs('./data_dir/published')
    app.run()