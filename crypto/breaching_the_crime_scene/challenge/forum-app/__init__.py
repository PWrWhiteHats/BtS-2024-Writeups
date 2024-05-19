import os
import requests
import ssl

from functools import wraps
from flask import Flask, request, render_template, abort, Response
from base64 import urlsafe_b64encode, urlsafe_b64decode, b64encode
from werkzeug.exceptions import HTTPException
import gzip


name = os.path.basename(os.path.dirname(__file__))
app = Flask(name)
app.config['SECRET_KEY'] = os.urandom(24)

app.config['PASSWORD'] = os.getenv('PASSWORD', b64encode(os.urandom(12)).decode('utf-8'))
app.config['FLAG'] = os.environ.get('FLAG', 'BtSCTF{this_is_a_fake_flag}')
app.config['IMG_APP_URL'] = "https://127.0.0.1:5001/"

error_color_map = {
    400: 'red',
    401: 'blue',
    403: 'green',
    404: 'orange',
    500: 'purple'
}

@app.after_request
def compress_response(response):
    response.direct_passthrough = False
    content = gzip.compress(response.get_data(), compresslevel=9)
    response.set_data(content)
    response.headers['Content-Encoding'] = "gzip"
    response.headers['Content-Length'] = len(response.get_data())
    return response

@app.errorhandler(HTTPException)
def handle_exception(e):
    with open('forum-app/static/resources/error/3.jpg', 'rb') as img:
        img = urlsafe_b64encode(img.read()).decode('utf-8')
    color = error_color_map.get(e.code, 'red')

    url = app.config['IMG_APP_URL'] + 'colorImage'
    data = f"image={img}&color={color}&password={app.config['PASSWORD']}"
    data = gzip.compress(data.encode('utf-8'), compresslevel=9)

    res = requests.post(url,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Encoding': 'gzip'},
            )
    
    if res.status_code == 200:
        img = b64encode(res.content).decode('utf-8')
    else:
        img = ""

    return render_template('error.html', error=e.code, img_base64=img, color=color), e.code

@app.errorhandler(404)
def page_not_found(e):
    with open('forum-app/static/resources/error/3.jpg', 'rb') as img:
        img = urlsafe_b64encode(img.read()).decode('utf-8')
    
    url = app.config['IMG_APP_URL'] + 'addTextImg'
    data = f"image={img}&text=404: {request.path}&password={app.config['PASSWORD']}"
    data = gzip.compress(data.encode('utf-8'), compresslevel=9)

    res = requests.post(url,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Encoding': 'gzip',
                     'Content-Length': str(len(data))},
            )
    
    if res.status_code == 200:
        img = b64encode(res.content).decode('utf-8')
    else:
        img = ""

    return render_template('error.html', error=404, img_base64=img, color=error_color_map[404]), 404

def authorization_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'password' not in request.form:
            abort(401)
        password = request.form['password']
        if password != app.config['PASSWORD']:
            abort(401)
        else:
            return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forum', methods=['POST'])
@authorization_required
def show_forum():
    return render_template('congrats.html', flag=app.config['FLAG'])
