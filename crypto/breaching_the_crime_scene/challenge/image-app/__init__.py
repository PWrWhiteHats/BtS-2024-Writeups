# Microservice for image manipulation
import os
import io
import ssl

from functools import wraps
from flask import Flask, request, abort
from base64 import urlsafe_b64encode, urlsafe_b64decode, b64encode
from PIL import Image, ImageColor, ImageDraw, ImageFont
import gzip


name = os.path.basename(os.path.dirname(__file__))
app = Flask(name)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PASSWORD'] = os.getenv('PASSWORD', b64encode(os.urandom(12)).decode('utf-8'))

@app.after_request
def compress_response(response):
    # we serve images, so we compress them
    response.direct_passthrough = False
    content = gzip.compress(response.get_data(), compresslevel=9)
    response.set_data(content)
    response.headers['Content-Encoding'] = "gzip"
    response.headers['Content-Length'] = len(response.get_data())
    return response

@app.before_request
def decompress_request():
    # requests contain images, so we expect them to be compressed
    if request.headers.get('Content-Encoding') == 'gzip':
        content = request.get_data()
        content = gzip.decompress(content)
        request._cached_data = content
        request.data = content

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

@app.route('/resizeImage', methods=['POST'])
@authorization_required
def resize_image():
    if 'width' not in request.form or 'height' not in request.form or 'image' not in request.form:
        abort(400)
    try:
        image = urlsafe_b64decode(request.form['image'])
        with Image.open(io.BytesIO(image), formats=["gif", "png"]) as img:
            width = request.json['width']
            height = request.json['height']
            img = img.resize((width,height), Image.Resampling.NEAREST)
            with io.BytesIO() as fp:
                img.save(fp, format='PNG')
                return fp.getvalue()
    except Exception as e:
        abort(500)

@app.route('/colorImage', methods=['POST'])
@authorization_required
def color_image():
    if 'image' not in request.form or 'color' not in request.form:
        abort(400)
    try:
        color = request.form['color']
        image = urlsafe_b64decode(request.form['image'])
        assert ImageColor.getrgb(color)
        with Image.open(io.BytesIO(image)) as img:
            mask = Image.new(img.mode, img.size, color=color)
            img = Image.blend(img, mask, 0.5)
            img = img.resize((200,200), Image.Resampling.NEAREST)
            with io.BytesIO() as fp:
                img.save(fp, format='PNG')
                return fp.getvalue()   
    except Exception as e:
        abort(500)

@app.route('/addTextImg', methods=['POST'])
@authorization_required
def add_text_img():
    if 'text' not in request.form or 'image' not in request.form:
        abort(400)
    try:
        text = request.form['text']
        if len(text) > 200:
            text = text[:200]
        image = urlsafe_b64decode(request.form['image'])
        with Image.open(io.BytesIO(image)) as img:
            font = ImageFont.load_default(size=20)
            img = img.resize((200,200), Image.Resampling.NEAREST)
            draw = ImageDraw.Draw(img)
            draw.text((100,30), text, fill='black', anchor='mm', align="center", font=font)
            with io.BytesIO() as fp:
                img.save(fp, format='PNG')
                return fp.getvalue()
    except Exception as e:
        abort(500)
