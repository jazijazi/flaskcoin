from flask import Flask
from base.config import Development
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# from flask_mail import Mail

from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin


from celery import Celery
from celery.utils.log import get_task_logger

from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object(Development)

#SOCKET
socketio = SocketIO(app)

# #EMAIL
# mail = Mail(app)

#Databese
db = SQLAlchemy(app)
migrate = Migrate(app , db)

# #Bcrypt
# bcrypt = Bcrypt(app)

#CELERY
logger = get_task_logger(__name__)
celery = Celery(app.name)
celery.config_from_object('base.config:Development')
celery.autodiscover_tasks()

# #Loginmanager
# login_manager = LoginManager(app)
# login_manager.login_view = 'users.login'
# login_manager.login_message = 'Please login to access this page!'
# login_manager.login_message_category = 'warning'

#Register Blueprints
from base.apps.coin_app import coins
# from directory.apps.posts_app import posts
# from directory.apps.errors_app import errors

app.register_blueprint(coins)
# app.register_blueprint(posts)
# app.register_blueprint(errors)

#ADMIN
from base.apps.admin_app import admin