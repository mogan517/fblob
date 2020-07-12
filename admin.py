from flask import Flask
from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskblog/site.db'
app.config['SECRET_KEY'] = 'mysecret'
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)
admin  =  Admin(app)

@app.route('/api', methods=['GET'])
def get():
    slist = Sitelist.query.all()
    output = []
    for site in slist:
        user_data = {}
        user_data['title'] = site.title
        user_data['content'] = site.content
        output.append(user_data)
    return jsonify({'user': output})

@app.route('/home')
def home():
    # return render_template('fruit.html')
    return "okoko123"
subs = db.Table('subs',
        db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
        db.Column('chanel_id', db.Integer, db.ForeignKey('chanel.chanel_id'))
        )
class Person(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(30))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # def __repr__(self):
    #     return f"Post('{self.title}', '{self.date_posted}')"

class Sitelist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(40), nullable=True)
    publisher = db.Column(db.String(80), nullable=True)
    likecount = db.Column(db.Integer, nullable=True)
    subtitle = db.Column(db.String(400), nullable=True)
    desc = db.Column(db.String(400), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=True)
class Postu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(400), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    # def __repr__(self):
    #     return f"Post('{self.title}', '{self.date_posted}')"
admin.add_view(ModelView(Person,db.session))
admin.add_view(ModelView(Post,db.session))
admin.add_view(ModelView(Postu,db.session))
admin.add_view(ModelView(Sitelist,db.session))

if __name__ == '__main__':
    # from waitress import serve
    # serve(app,host='0.0.0.0',port=8000)
    app.run(port=5002, debug=True)
