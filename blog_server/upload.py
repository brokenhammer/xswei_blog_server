from blog_server import app
import json

@app.route('/upload_img', methods=["POST"])
def upload_img():
    print('receiving...')
    ret_json = {'success':1, 'message': 'recieved', 'url':'http://image170-c.poco.cn/mypoco/myphoto/20171228/08/17870440420171228085409096_640.jpg?1280x1920_120'}
    json_str = json.dumps(ret_json)
    return json_str