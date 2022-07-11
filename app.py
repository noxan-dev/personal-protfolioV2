from flask import Flask, render_template
from flask_caching import Cache
from datetime import datetime
import os
import requests


cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# parmas = {
#     'client_id': '5596470317044314',
#     'redirect_uri': 'https://chaimswebsite.herokuapp.com/',
#     'scope': 'user_profile,user_media',
#     'response_type': 'code'
# }
# response = requests.get('https://api.instagram.com/oauth/authorize', params=parmas)
# print(response.url)


@app.template_filter('remove_dashes')
def remove_dashes(string):
    return string.replace('-', ' ')


@app.template_filter('upper')
def upper(string):
    return string.title()


@app.route('/')
# @cache.cached(timeout=60)
def redesign():
    year = datetime.now().year
    return render_template('indexV2.html', year=year)


@app.route('/about')
# @cache.cached(timeout=60)
def about():
    return render_template('about.html')


@app.route('/projects')
@cache.cached(timeout=60)
def projects():
    response = requests.get('https://api.github.com/users/noxan-dev/repos')
    repos_json = response.json()
    repo_names = []
    for repo in repos_json:
        repo_names.append(repo['name'])
    return render_template('projects.html', repos=repos_json, repo_names=repo_names)


if __name__ == '__main__':
    app.run()
