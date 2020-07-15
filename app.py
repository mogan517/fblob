from flask import Flask
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

template_dir = os.path.abspath('./flaskblog/templates')
app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = 'dev'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskblog/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ckeditor = CKEditor(app)


class Sitelist(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(40), nullable=True)
    publisher = db.Column(db.String(80), nullable=True)
    likecount = db.Column(db.Integer, nullable=True)
    subtitle = db.Column(db.String(400), nullable=True)
    desc = db.Column(db.String(400), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.Text)


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Go to Admin!</a>'


# Customized Post model admin
class PostAdmin(ModelView):
    # override form type with CKEditorField
    form_overrides = dict(text=CKEditorField)
    create_template = 'edit.html'
    edit_template = 'edit.html'

class SiteAdmin(ModelView):
    # override form type with CKEditorField
    form_overrides = dict(content=CKEditorField)
    create_template = 'edit.html'
    edit_template = 'edit.html'


admin = Admin(app, name='Flask-CKEditor demo')
admin.add_view(PostAdmin(Post, db.session))
admin.add_view(SiteAdmin(Sitelist, db.session))


def init_db():
    """
    Populate a small db with some example entries.
    """
    db.drop_all()
    db.create_all()

    # Create sample Post
    title = "de Finibus Bonorum et Malorum - Part I"
    text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor \
                incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud \
                exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure \
                dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. \
                Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt \
                mollit anim id est laborum."

    post = Post(title=title, text=text)
    db.session.add(post)
    db.session.commit()


if __name__ == '__main__':
    # init_db()
    app.run(debug=True)
