import os

from flask import Flask, render_template, request, redirect, flash
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from db.db import db
from models.app_model import Profile

app = Flask(__name__)
app.secret_key = 'asrtarstaursdlarsn'
app.config.from_object('settings.Config')
app.config["IMAGE_UPLOADS"] = "./static/images/profiles"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

# initialization
db.init_app(app)


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        image = request.files["img_name"]
        if image.filename == "":
            flash('Please Upload Image file', "danger")
            return redirect(request.url)
        if allowed_image(image.filename):
            filename = secure_filename(image.filename)
            try:
                profile_entry = Profile(img_name=filename)
                db.session.add(profile_entry)
                db.session.commit()
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                flash('File upload Successfully !', "success")
            except IntegrityError as e:
                flash('Something went wrong please try again later', "danger")
                return redirect(request.url)
        else:
            flash('That file extension is not allowed', "danger")
            return redirect(request.url)
    profiles = Profile.query.all()
    return render_template('index.html', profiles=profiles)


# run always put in last statement or put after all @app.route
if __name__ == '__main__':
    app.run(host='localhost')
