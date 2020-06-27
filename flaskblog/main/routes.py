from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route('/article/<int:aid>')
def article(aid):
    cur = mysql.connection.cursor()
    resultValue1 = cur.execute('SELECT * FROM Articles WHERE ArticleId = {0}'.format(aid))
    article = cur.fetchall()
    return render_template('article.html', article=article, aid=aid)
@main.route('/articlelist')
def articlelist():
    # cur = mysql.connection.cursor()
    # resultValue1 = cur.execute('SELECT * FROM Articles')
    # allarticle = cur.fetchall()
    return render_template('article.html')
@main.route('/users')
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

@main.route("/registration",methods=['GET','POST'])
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
        return redirect('/users')
    return render_template('regist.html')

