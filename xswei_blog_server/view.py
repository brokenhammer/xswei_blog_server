from xswei_blog_server import app
from flask import render_template,request,redirect,url_for
import os,datetime
import urllib.parse
@app.route("/")
def root():
    return redirect(url_for("list_blog"))

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

@app.route("/list_drafts")
def list_drafts():
    return render_template('list_drafts.html')

@app.route("/list_blog")
def list_blog():
    return render_template('list_blog.html')

@app.route("/blog_view/<path:save_name>")
def blog_view(save_name):
    return render_template('blog_view.html',blog_path=save_name)