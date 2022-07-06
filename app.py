from flask import Flask, render_template
from flask_caching import Cache
from datetime import datetime

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
    year = datetime.now().year
    return render_template('indexV2.html', year=year)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.229', port=5000)
