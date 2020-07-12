from flask import Flask, current_app
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_admin.menu import MenuLink
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flaskblog.config import Config
from flask_admin.contrib.sqla import ModelView
db = SQLAlchemy()
admin = Admin()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
mysql = MySQL()
# with current_app.open_resource('static/root.txt') as f:
    # f.read()
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config["MYSQL_HOST"] = '47.101.59.109'
    app.config["MYSQL_PORT"] = 3306
    app.config["MYSQL_USER"] = 'mogan'
    app.config["MYSQL_PASSWORD"] = 'nease.net'
    app.config["MYSQL_DB"] = 'flaskapp'
    app.config.from_object(Config)
    mysql.init_app(app)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    # admin.init_app(app,index_view=users)
    # admin.add_link(MenuLink(name='Home', url='/'))
    # admin.add_link(MenuLink(name='Logout', url='/logout'))
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    # app.register_blueprint(admin)

    return app
