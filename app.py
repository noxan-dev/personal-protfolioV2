from flask import Flask, render_template
from flask_caching import Cache
from datetime import datetime
import os


cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route('/')
# @cache.cached(timeout=60)
def redesign():
    year = datetime.now().year
    return render_template('indexV2.html', year=year)


@app.route('/about')
# @cache.cached(timeout=60)
def about():
    return render_template('about.html')


@app.route('/contact')
# @cache.cached(timeout=60)
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
