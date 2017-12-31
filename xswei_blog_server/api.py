from xswei_blog_server import app
import os
from flask import send_from_directory

@app.route("/api/get_all_blogs")
def get_all_blogs():
    return send_from_directory(os.getcwd(), app.config['BLOGS_INDEX'])

@app.route("/api/get_all_drafts")
def get_all_drafts():
    return send_from_directory(os.getcwd(), app.config['DRAFTS_INDEX'])