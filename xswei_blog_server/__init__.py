#/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from flask import Flask
import json

app = Flask(__name__)
if not os.path.exists('./data_dir/drafts'):
    os.makedirs('./data_dir/drafts')
if not os.path.exists('./data_dir/published'):
    os.makedirs('./data_dir/published')
if not os.path.exists('./data_dir/published/index.json'):
    with open('./data_dir/published/index.json', 'w') as j:
        json.dump([], j)
if not os.path.exists('./data_dir/drafts/index.json'):
    with open('./data_dir/drafts/index.json', 'w') as j:
        json.dump([], j)
import xswei_blog_server.view, xswei_blog_server.api, xswei_blog_server.auth_view
