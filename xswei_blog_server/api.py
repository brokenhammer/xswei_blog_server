from xswei_blog_server import app
import os, json
from flask import url_for,send_from_directory
from xswei_blog_server.utils import parse_path


@app.route("/api/get_all_blogs")
def get_all_blogs():
    with open('data_dir/published/index.json', 'r', encoding='utf-8') as f:
       return f.read()
    #return send_from_directory(os.getcwd(),'data_dir/published/index.json')
    years = os.listdir('data_dir/published')
    blog_set = []
    for y in years:
        months = os.listdir('data_dir/published/{}'.format(y))
        for m in months:
            days = os.listdir('data_dir/published/{}/{}'.format(y, m))
            for d in days:
                flist = os.listdir('data_dir/published/{}/{}/{}'.format(y, m, d))
                for f in flist:
                    if os.path.splitext(f)[1] == '.md':
                        title = os.path.splitext(f)[0]
                        blog_set.append('{}/{}/{}/{}'.format(y, m, d, title))
    blog_set.sort(reverse=True)
    ret_list = []
    for save_name in blog_set:
        title = save_name.split('/')[-1]
        pub_date = save_name.split('/')[0:3]
        ret_list.append({'link':save_name, 'title': title,
                         'edit_link': url_for('edit',fpath=save_name, md_type='blog'),
                         'delete_link': url_for('delete_blog',save_name=save_name),
                         'Y': pub_date[0], 'M': pub_date[1], 'D': pub_date[2]})
    json_str=json.dumps(ret_list)
    return json_str

@app.route("/api/get_all_drafts")
def get_all_drafts():
    print(os.getcwd())
    #with open('data_dir/drafts/index.json', 'r', encoding='utf-8') as f:
    #  return f.read()
    return send_from_directory(os.getcwd(), 'data_dir/drafts/index.json')
    file_list = os.listdir('data_dir/drafts')
    ret_dict = []
    for save_name in file_list:
        save_name = os.path.splitext(save_name)[0]
        y,m,d,title = parse_path(save_name, md_type='draft')
        ret_dict.append({'link': save_name, 'title': title,
                         'edit_link':url_for('edit',fpath=save_name, md_type='draft'),
                         'delete_link':url_for('delete_drafts',save_name=save_name),
                         'Y': y, 'M': m, 'D': d})
    json_str=json.dumps(ret_dict)
    return json_str