from flask import Flask, render_template, flash, redirect, url_for, request
from flask_caching import Cache
from datetime import datetime
import os
import requests
import smtplib

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

MAIL_USERNAME = 'chaimmalek@gmail.com'
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']


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


@app.route('/', methods=['GET', 'POST'])
# @cache.cached(timeout=60)
def redesign():
    year = datetime.now().year

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        if name == '' or email == '' or message == '':
            flash('Please fill in all fields.')
            return redirect(url_for('redesign'))
        else:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
                smtp.sendmail(from_addr=email,
                              to_addrs=MAIL_USERNAME,
                              msg='Subject: New Message from {}\n\n{}\n{}'.format(name, message, email)
                              )
            flash('Message sent!')
            return redirect(url_for('redesign'))
    return render_template('indexV2.html', year=year)


@app.route('/about')
# @cache.cached(timeout=60)
def about():
    return render_template('about.html')


@app.route('/projects')
# @cache.cached(timeout=60)
def projects():
    response = requests.get('https://api.github.com/users/noxan-dev/repos')
    repos_json = response.json()
    return render_template('projects.html', repos=repos_json)


if __name__ == '__main__':
    app.run()
