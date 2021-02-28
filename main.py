from flask import Flask, render_template, url_for, request, session, redirect, flash, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
menu = ["Download", "First app", "Contact us"]
secret_key = 'The most secret key ever'
app.config['SECRET_KEY'] = secret_key


# vars for html
success = 'alert-success'
error = 'alert-danger'


# db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
date_now = datetime.utcnow().strftime("%b %d %Y")
print(date_now)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.String(3000), nullable=False)
    date = db.Column(db.String(15), default=date_now)

    def __repr__(self):
        return '<Article %r>' % self.id


# home page
@app.route('/home')
@app.route('/')
def index():
    print(url_for('index'))
    return render_template("index.html", title='Home')


# about page
@app.route('/about')
def about():
    print(url_for('about'))
    return render_template("about.html", title="About", menu=menu)


# contact page
@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if len(request.form['username']) > 2:
            flash('Your message has been successfully sent.', category=success)
        else:
            flash('Error! Check that the data you entered is correct. ', category=error)
        print(request.form['username'])

    return render_template("contact.html", title="Contact us")


# login page
@app.route('/login', methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == "POST" and (request.form['username'] == 'admin' and request.form['password'] == '123'):
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    else:
        return render_template('login.html')


# profile page
@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"User: {username}"


# posts
@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.id.desc()).all()
    return render_template('posts.html', articles=articles)


# post detail page
@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


# create article
@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'An error occurred while adding the article'
    else:
        return render_template('create_article.html')


# page not found error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title="Page not found"), 404


if __name__ == "__main__":
    app.run(debug=True)
