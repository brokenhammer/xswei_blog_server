from blog_server import app


# cannot sendfile hear because the browser will cache it
@app.route("/api/get_all_blogs")
def get_all_blogs():
    with open(app.config['BLOGS_INDEX'], 'r', encoding='utf-8') as f:
        return f.read()

@app.route("/api/get_all_drafts")
def get_all_drafts():
    with open(app.config['DRAFTS_INDEX'], 'r', encoding='utf-8') as f:
        return f.read()