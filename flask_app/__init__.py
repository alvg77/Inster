from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_whooshee import Whooshee
import os

app = Flask(__name__)
whooshee = Whooshee(app)
whooshee.reindex()
app.config['SECRET_KEY'] = 'c78119002dc96180e56f64c789a7d732b74c83dd23d63be147'
bcrypt = Bcrypt()
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://fsjvniytpfyucz:767f0e79306a31257018002b6fed9ada05f578e00c6e68f51e6e746d55cdfc2f@ec2-52-213-167-210.eu-west-1.compute.amazonaws.com:5432/d8mdtd68aeqmm4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "no1515783@gmail.com"
app.config['MAIL_PASSWORD'] = 'qazwsxedc741852963'
mail = Mail(app)

from flask_app import routes