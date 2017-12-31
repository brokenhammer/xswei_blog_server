#/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from flask import Flask
from xswei_blog_server.utils import sync_jsonDB_published, sysn_jsonDB_drafts, before_run

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.config['WORK_DIR'] = os.getcwd()
before_run(app.config)

import xswei_blog_server.view, xswei_blog_server.api, xswei_blog_server.auth_view
