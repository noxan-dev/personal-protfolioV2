from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_caching import Cache
from datetime import datetime
import os
import smtplib


UPLOAD_FOLDER = os.path.join('static', 'images/gallery')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


MAIL_USERNAME = 'chaimmalek@gmail.com'
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']


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
                              msg='Subject: New Message from {}\n\n{}\nFrom: {}'.format(name, message, email)
                              )
            flash('Message sent!')
            return redirect(url_for('redesign'))
    return render_template('indexV2.html', year=year)


@app.route('/about')
# @cache.cached(timeout=60)
def about():
    return render_template('about.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     # TODO: make so I can only upload an image
#     # TODO: Add a delete option
#     if request.method == 'POST' and 'photo' in request.files:
#         photos.save(request.files['photo'])
#         flash("Photo saved.")
#         return redirect(url_for('redesign'))
#     return render_template('upload.html')


@app.route('/gallery')
# @cache.cached(timeout=60)
def gallery():
    # TODO: Display all images in a gallery
    images_file = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html', images=images_file)


if __name__ == '__main__':
    app.run()
