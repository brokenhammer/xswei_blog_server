import os
import json


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
                print(blog_list)

    # years = os.listdir(config['BLOGS_DIR'])
    # blog_list = []
    # for y in years:
    #     if not os.path.isdir('{}/{}'.format(config['BLOGS_DIR'],y)):
    #         continue
    #     months = os.listdir('{}/{}'.format(config['BLOGS_DIR'],y))
    #     for m in months:
    #         days = os.listdir('{}/{}/{}'.format(config['BLOGS_DIR'], y, m))
    #         for d in days:
    #             flist = os.listdir('{}/{}/{}/{}'.format(config['BLOGS_DIR'], y, m, d))
    #             for f in flist:
    #                 #if os.path.splitext(f)[1] == '.md':
    #                 title = f
    #                 blog_list.append('{}/{}/{}/{}'.format(y, m, d, title))
    records=[]

    with open(config['BLOGS_INDEX'], 'w', encoding='utf-8') as j:
        for save_name in blog_list:
            records.append(save_name)
        json.dump(records, j)

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


