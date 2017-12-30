import json
import uuid
def add_item(y,m,d,title,fpath,jsonpath):
    #TODO: lock
    id = uuid.uuid4()
    item = {'year': y,
            'month': m,
            'day': d,
            'title': title,
            'path': fpath}
    with open(jsonpath, 'r') as f:
        records = json.load(f)

    records[id] = item

    with open(jsonpath, 'w') as f:
        json.dump(records, f)

def del_item(jsonpath,id):
    with open(jsonpath, 'r') as f:
        records = json.load(f)
    records.pop(id)
    with open(jsonpath, 'w') as f:
        json.dump(records, f)

