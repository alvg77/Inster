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
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://nvokfcclwwczpc:9495b28576af9f4264baae945dd2e6851edb90050c94a6e881646b23fb6c7b58@ec2-54-216-48-43.eu-west-1.compute.amazonaws.com:5432/d9rljm0j9qffsn"
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