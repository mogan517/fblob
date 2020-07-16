import os
from flask import render_template, request, Blueprint, redirect, url_for
from flaskblog.models import Post,Sitelist
main = Blueprint('main', __name__)
from flaskblog import mysql # Import from app here

@main.route("/")
def newhome():
    list = Sitelist.query.all()
    # list = Sitelist.query.filter_by(id=2).first()
    # for r in list:
    #     print(r)
    return render_template('newhome.html',list=list)
@main.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))

@main.route('/root.txt')
def roott():
    return redirect(url_for('static', filename='root.txt'))

# @main.route('/favicon.ico')
# def favicon():
#     print(75)
#     return send_from_directory(os.path.join(main.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon') 
@main.route("/bitch")
def getArticle():
    list = Sitelist.query.all()
    # list = Sitelist.query.filter_by(id=title).first()
    print(list)
    # return f' oko is : {list.title}'
    return render_template('index.html', list=list)
@main.route('/usersa')
def userss():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)
@main.route("/blog/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/blog/about")
def abouts():
    print(777777777771)
    return render_template('about.html', title='About')
@main.route("/about")
def about():
    print(777777777778)
    return render_template('index.html', title='About')

@main.route('/article/<int:aid>')
def article(aid):
    list = Sitelist.query.filter_by(id=aid).first()
    cur = mysql.connection.cursor()
    resultValue1 = cur.execute('SELECT * FROM Articles WHERE ArticleId = {0}'.format(aid))
    article = cur.fetchall()
    return render_template('article.html', article=article, aid=aid, list=list)
@main.route('/articlelist')
def articlelist():
    # cur = mysql.connection.cursor()
    # resultValue1 = cur.execute('SELECT * FROM Articles')
    # allarticle = cur.fetchall()
    return render_template('article.html')
@main.route('/blog/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)
@main.route("/postarticle", methods=['GET', 'POST'])
def postarticle():
    if request.method == "POST":
        userPost = request.form
        title = userPost['Title']
        photo = userPost['Photo']
        img = convertToBinaryData(photo)
        ss = userPost['Snapshot']
        content = userPost['Content']
        cur = mysql.connection.cursor()
        insert_stmt = (
          "INSERT INTO Articles (Photo,Title,Content,Snapshot) "
          "VALUES (%s,%s,%s,%s)"
        )
        cur.execute(insert_stmt, [img, title, content, ss])
        mysql.connection.commit()
        cur.close()
    return render_template('postarticle.html')

@main.route("/blog/registration",methods=['GET','POST'])
def registration():
    if request.method == "POST":
        userDetails  = request.form
        name = userDetails['name']
        email = userDetails['email']
        msg = userDetails['msg']
        cur = mysql.connection.cursor()
        insert_stmt = (
          "INSERT INTO users (name,email,msg) "
          "VALUES (%s,%s,%s)"
        )
        cur.execute(insert_stmt, [name,email,msg])
        mysql.connection.commit()
        cur.close()
        return redirect('/blog/users')
    return render_template('regist.html')

