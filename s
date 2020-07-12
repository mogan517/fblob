from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskblog/site.db'
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)
admin  =  Admin(app)
subs = db.Table('subs',
        db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
        db.Column('chanel_id', db.Integer, db.ForeignKey('chanel.chanel_id'))
        )
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(30))
    subscriptions = db.relationship('Chanel', secondary=subs, backref=db.backref('subscribers', lazy='dynamic'))
class Chanel(db.Model):
    chanel_id = db.Column(db.Integer, primary_key=True)
    chanel_name = db.Column(db.String(30))


admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Chanel,db.session))
