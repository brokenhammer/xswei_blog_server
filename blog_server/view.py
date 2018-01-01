from blog_server import app
from flask import render_template,redirect,url_for,abort
import urllib.parse
from blog_server.utils import legal_path, full_path


@app.route("/")
def root():
    return redirect(url_for("list_blog"))

@app.route("/load_blog_md/<md_type>/<path:fpath>")
def data_request(fpath, md_type):
    fpath = urllib.parse.unquote(fpath)
    fpath = legal_path(fpath, md_type)
    if not fpath:
        abort(404)
    full_fpath = full_path(fpath, md_type, app.config)
    full_fname = full_fpath + '.md'
    with open(full_fname,'r',encoding='utf-8') as f:
        return f.read()

@app.route("/list_drafts")
def list_drafts():
    return render_template('list_drafts.html')

@app.route("/list_blog")
def list_blog():
    return render_template('list_blog.html')

@app.route("/blog_view/<md_type>/<path:fpath>")
def blog_view(fpath,md_type):
    return render_template('blog_view.html',fpath=fpath, md_type=md_type)