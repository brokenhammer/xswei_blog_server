from blog_server import app
from flask import redirect,request, url_for
import json
from blog_server.utils import same_host, upload_want, allowed_file, want_url
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

@app.route('/upload_img', methods=["POST"])
def upload_img():
    ret_json = {'success': 0, 'message': '', 'url': ''}
    file = request.files['editormd-image-file']
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        extension = filename.rsplit('.', 1)[1]
        upload_name = upload_want(file, extension, app.config)
        if upload_name: # success
            ret_json = {'success':1, 'message':'received', 'url': url_for('serve_img', img_name=upload_name)}
    else:
        ret_json['message'] = 'Failed!'
    json_str = json.dumps(ret_json)
    return json_str


@app.route('/blog_img/<img_name>')
def serve_img(img_name):
    good_referrer = 'http://{}/'.format(request.host)
    if not (request.referrer and same_host(request.referrer, good_referrer)):
        return redirect('https://www.baidu.com/img/baidu_jgylogo3.gif') #fake image
    url = want_url(img_name, app.config)
    return redirect(url)