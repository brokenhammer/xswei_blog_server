#/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from flask import Flask
app = Flask(__name__)
if not os.path.exists('./data_dir/drafts'):
    os.makedirs('./data_dir/drafts')
if not os.path.exists('./data_dir/published'):
    os.makedirs('./data_dir/published')
import xswei_blog_server.view, xswei_blog_server.api
