from flask import Flask, render_template, url_for
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)

cache.init_app(app)
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'secret!'
TEMPLATES_AUTO_RELOAD = True


@app.route('/')
@cache.cached(timeout=60)
def home():
    return render_template('index.html')


@app.route('/redesign')
# @cache.cached(timeout=60)
def redesign():
    return render_template('indexV2.html')


if __name__ == '__main__':
    app.run(debug=True)
