from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_uploads import IMAGES, UploadSet , configure_uploads , patch_request_class
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://samar:samar@localhost/project"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sjcghggkggvuusvgsvgsk'
app.config['UPLOAD_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
# photos = UploadSet('photos' , IMAGES)
# configure_uploads(app , photo)
# patch_request_clas(app)

db = SQLAlchemy(app)


from FlaskApp import models
from FlaskApp import routes

db.create_all()