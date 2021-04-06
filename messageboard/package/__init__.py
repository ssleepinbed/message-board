"""
The Init file
"""
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "G:/web/Website/package/static/userimages"
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}

app = Flask(__name__)
csrf = CSRFProtect(app)

###APP CONFIGURATION
app.config['SECRET_KEY'] = '92c8c31d2eee59cd709109a14ed68590'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginmanager = LoginManager(app)

from package import routes
from package.models import User