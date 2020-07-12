from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskblog/site.db'
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)
manymore = Admin(app)
subs = db.Table('subs',
        db.Column('user_id', db.Integer, db.ForeignKey('puser.user_id')),
        db.Column('chanel_id', db.Integer, db.ForeignKey('chanel.chanel_id'))
        )
class Puser(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    subscriptions = db.relationship('Chanel', secondary=subs, backref='subscribers', lazy='dynamic')
class Chanel(db.Model):
    chanel_id = db.Column(db.Integer, primary_key=True)
    chanel_name = db.Column(db.String(30))
class Ifile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)


manymore.add_view(ModelView(Puser, db.session))
# manymore.add_view(ModelView(Subs, db.session))
# manymore.add_view(ModelView(Chanel, db.session))

@app.route('/')
def home():
    slist = Puser.query.all()
    output = []
    for site in slist:
        user_data = {}
        user_data['name'] = site.name
        output.append(user_data)
    # return jsonify({'user': output})
    return render_template('test.html')
@app.route('/upload', methods=["POST"])
def upload():
    file =  request.files['inputFile']
    newFile = FileContents(name=file.filename,data=file.read())
    db.session.add(newFile)
    db.session.commit()
@app.route('/download')
def download():
    file_data = FileContents.query.filter_by(id=1),frist()
    return send_file = FileContents.query.filter_by(id=1).first()
if __name__ == '__main__':
    # from waitress import serve
    # serve(app,host='0.0.0.0',port=8000)
    app.run(port=5001, debug=True)
