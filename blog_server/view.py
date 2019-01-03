from blog_server import app
from flask import render_template,redirect,url_for,abort,send_file,send_from_directory
import urllib.parse,os
from blog_server.utils import legal_path, full_path, parse_path


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

@app.route("/load_blog_html/<path:fpath>")
def html_request(fpath):
    fpath = urllib.parse.unquote(fpath)
    fpath = legal_path(fpath, 'blog')
    if not fpath:
        abort(404)
    full_fpath = full_path(fpath, 'blog', app.config)
    full_fname = full_fpath + '.html'
    with open(full_fname, 'r', encoding='utf-8') as f:
        return f.read()

@app.route("/list_drafts")
def list_drafts():
    return render_template('list_drafts.html',title="所有草稿")

@app.route("/list_blog")
def list_blog():
    return render_template('list_blog.html',title="所有文章")

@app.route("/blog_view/<md_type>/<path:fpath>")
def blog_view(fpath,md_type):
    fpath = legal_path(fpath, md_type)
    if not fpath:
        abort(404)
    y, m, d, title = parse_path(fpath, md_type)
    return render_template('blog_view.html',fpath=fpath, md_type=md_type,
                           title=title)

@app.route("/zip_blogs")
def zip_blogs():
    import tempfile
    import zipfile
    #tmp = tempfile.mktemp()
    #tmp += '.zip'
    tmp = 'blogs.zip'
    with zipfile.ZipFile(tmp,'w') as zf:
        for dirpath, dirnames, filenames in os.walk('data_dir/published'):
            for fname in filenames:
                zf.write(os.path.join(dirpath,fname))
    return send_from_directory(os.getcwd(),tmp)
