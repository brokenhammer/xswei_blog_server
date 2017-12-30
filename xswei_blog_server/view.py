from xswei_blog_server import app
from flask import render_template,request,redirect,url_for,abort
import os,datetime
import urllib.parse
from xswei_blog_server.utils import legal_path


@app.route("/")
def root():
    return redirect(url_for("list_blog"))

@app.route("/load_blog_md/<md_type>/<path:fpath>")
def data_request(fpath, md_type):
    fpath = urllib.parse.unquote(fpath)
    fpath = legal_path(fpath, md_type)
    if not fpath:
        abort(404)
    if md_type == 'draft':
        save_dir = 'data_dir/drafts/'
    elif md_type == 'blog':
        save_dir = 'data_dir/published/'
    else:
        abort(404)
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