import os

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
