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

def sysn_jsonDB_drafts(jsonpath):
    file_list = os.listdir('data_dir/drafts')
    records = []
    with open(jsonpath, 'w', encoding='utf-8') as j:
        for save_name in file_list:
            if os.path.splitext(save_name)[1] == '.md':
                save_name = os.path.splitext(save_name)[0]
                records.append(save_name)
        json.dump(records, j)

def sync_jsonDB_published(jsonpath):
    years = os.listdir('data_dir/published')
    blog_list = []
    for y in years:
        months = os.listdir('data_dir/published/{}'.format(y))
        for m in months:
            days = os.listdir('data_dir/published/{}/{}'.format(y, m))
            for d in days:
                flist = os.listdir('data_dir/published/{}/{}/{}'.format(y, m, d))
                for f in flist:
                    if os.path.splitext(f)[1] == '.md':
                        title = os.path.splitext(f)[0]
                        blog_list.append('{}/{}/{}/{}'.format(y, m, d, title))
    records=[]
    with open(jsonpath, 'w', encoding='utf-8') as j:
        for save_name in blog_list:
            if os.path.splitext(save_name)[1] == '.md':
                save_name = os.path.splitext(save_name)[0]
                records.append(save_name)
        json.dump(records, j)

