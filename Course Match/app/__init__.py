from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

#Database/app config
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views, models

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)