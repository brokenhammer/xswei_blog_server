#/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from flask import Flask
from blog_server.utils import sync_jsonDB_published, sysn_jsonDB_drafts, before_run
from flask_cors import CORS


app = Flask(__name__, instance_relative_config=True)
CORS(app)
app.config.from_object('config')
app.config['WORK_DIR'] = os.getcwd()
if os.path.exists('instance/config.py'):
    app.config.from_pyfile('config.py')
before_run(app.config)

import blog_server.view, blog_server.api, blog_server.auth_view, blog_server.upload

