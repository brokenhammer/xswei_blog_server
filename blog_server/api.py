from blog_server import app
import os
from flask import send_from_directory

@app.route("/api/get_all_blogs")
def get_all_blogs():
    if app.config['DEBUG'] is False:
        return send_from_directory(os.getcwd(), app.config['BLOGS_INDEX'])
    else:
        with open(app.config['BLOGS_INDEX'], 'r', encoding='utf-8') as f:
            return f.read()

@app.route("/api/get_all_drafts")
def get_all_drafts():
    if app.config['DEBUG'] is False:
        return send_from_directory(os.getcwd(), app.config['DRAFTS_INDEX'])
    else:
        with open(app.config['DRAFTS_INDEX'], 'r', encoding='utf-8') as f:
            return f.read()