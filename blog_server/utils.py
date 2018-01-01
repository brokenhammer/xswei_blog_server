import os
import json
import uuid
from urllib.parse import urlparse
from want import Want
import time
import hashlib

def legal_path(fpath, md_type):
    if md_type == 'blog':
        lists = fpath.split('/')
        year, month, day = lists[0:3]
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return None
        title = lists[3:]
        title = '／'.join(title)
        title.replace('\\','＼')
        return ('/').join((year, month, day, title))
    elif md_type == 'draft':
        return fpath.replace('/','／') .replace('\\','＼')
    else:
        return None

def construct_fpath(title, y, m, d, md_type):
    if md_type == 'draft':
        return legal_path('{}-{}-{}-{}'.format(y,m,d,title), md_type)
    elif md_type == 'blog':
        return legal_path('{}/{}/{}/{}'.format(y,m,d,title), md_type)

def full_path(fpath, md_type, config):
    if md_type == 'blog':
        root = config['BLOGS_DIR']
        fpath = legal_path(fpath, md_type)
        return os.path.join(root, fpath)
    elif md_type == 'draft':
        root = config['DRAFTS_DIR']
        return os.path.join(root, fpath)

def parse_path(fpath, md_type):
    if not legal_path(fpath, md_type):
        return None
    if md_type == 'blog':
        year, month, day, title = fpath.split('/')
    elif md_type == 'draft':
        lists = fpath.split('-')
        year, month, day = lists[0:3]
        title = lists[3:]
        title = '-'.join(title)

    return (year, month, day, title)

def add_item(jsonpath, fpath):

    with open(jsonpath, 'r', encoding='utf-8') as f:
        records = json.load(f)
    blog_set = set(records)
    blog_set.add(fpath)
    records = list(blog_set)
    with open(jsonpath, 'w', encoding='utf-8') as f:
        json.dump(records, f)

def del_item(jsonpath,fpath):
    with open(jsonpath, 'r', encoding='utf-8') as f:
        records = json.load(f)
    blog_set = set(records)
    if not fpath in (blog_set):
        return
    blog_set.remove(fpath)
    records = list(blog_set)
    with open(jsonpath, 'w', encoding='utf-8') as f:
        json.dump(records, f)

def sysn_jsonDB_drafts(config):
    file_list = os.listdir(config['DRAFTS_DIR'])
    records = []
    with open(config['DRAFTS_INDEX'], 'w', encoding='utf-8') as j:
        for save_name in file_list:
            if os.path.splitext(save_name)[1] == '.md':
                save_name = os.path.splitext(save_name)[0]
                records.append(save_name)
        json.dump(records, j)

def sync_jsonDB_published(config):
    blog_list = []
    for root, dirs, flist in os.walk(config['BLOGS_DIR']):
        for fname in flist:
            if fname.endswith('.md'):
                title = os.path.splitext(fname)[0]
                dir_name = root.replace('\\','/')
                y, m, d = dir_name.split('/')[-3:]
                blog_list.append('{}/{}/{}/{}'.format(y, m, d, title))

    with open(config['BLOGS_INDEX'], 'w', encoding='utf-8') as j:
        json.dump(blog_list, j)

def before_run(config):
    if not os.path.exists(config['DRAFTS_DIR']):
        os.makedirs(config['DRAFTS_DIR'])
    if not os.path.exists(config['BLOGS_DIR']):
        os.makedirs(config['BLOGS_DIR'])
    sysn_jsonDB_drafts(config)
    sync_jsonDB_published(config)
    create_root(config)

def create_root(config):
    from flask.ext.login import UserMixin
    import pickle
    root_user = UserMixin()
    root_user.id = 1
    with open(config['ROOT_FILE'], 'wb') as f:
        pickle.dump(root_user, f)

def same_host(requested, good):
    parsed_requested = urlparse(requested)
    parsed_good = urlparse(good)

    if not (parsed_good.scheme == parsed_requested.scheme and
            parsed_good.netloc == parsed_requested.netloc):
        return False
    return True

def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload_want(file, ext, config):
    filename = file.filename
    content = file.read()
    img_name = str(uuid.uuid4())
    full_name = '.'.join((img_name, ext))
    ws = Want(config['WANT_AK'], config['WANT_PK'])
    # 正常策略
    ps = {'detectMime': 1, 'expiration': int(time.time()*1000) + 3600 *1000, 'insertOnly': 0,
          'namespace': config['WANT_NAMESPACE'], 'sizeLimit': 0}
    upload_msg =  ws.upload_content(ps, config['WANT_DIR'], full_name, content)
    if upload_msg['code'] == 200:
        return upload_msg['name']
    return None

def want_url(img_name, config):

    width = '600'
    prefix = config['WANT_NAMESPACE']
    img_pk = config['WANT_IMG_PK']
    URI = '/{}/{}@{}w_1l'.format(config['WANT_DIR'], img_name, width)
    expiration = str(int(time.time() + 3600))
    rand = uid = '0'
    sstring = '-'.join((URI, expiration, rand, uid, img_pk))
    m5 = hashlib.md5()
    m5.update(sstring.encode())
    md5hash = m5.hexdigest()
    return 'http://{}.image.alimmdn.com{}?auth_key={}-{}-{}-{}'.format(prefix, URI, expiration, rand, uid, md5hash)




