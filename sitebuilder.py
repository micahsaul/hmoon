from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from motionless import DecoratedMap, AddressMarker
from PIL import Image
from StringIO import StringIO
import requests
import sys


DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'

app = Flask(__name__)
app.config.from_object(__name__)
posts = FlatPages(app)
freezer = Freezer(app)


def get_image(address, outfile):
    dmap = DecoratedMap(zoom=12, size_x=640, size_y=200, maptype='hybrid')
    dmap.add_marker(AddressMarker(address))
    response = requests.get(dmap.generate_url())
    img = Image.open(StringIO(response.content)).convert('L')
    img.save(outfile)


@app.route('/')
def index():
    return render_template('index.html', posts=posts)


@app.route('/<path:path>/')
def post(path):
    post = posts.get_or_404(path)
    return render_template('post.html', post=post, posts=posts)

if __name__ == '__main__':
    for post in posts:
        address = post['address']
        outfile = 'static/img/' + str(post['date']) + '-' + post['slug'] + '.png'
        get_image(address, outfile)
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.run(debug=True)
    else:
        app.run(port=8000)
