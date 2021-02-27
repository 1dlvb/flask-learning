import sqlite3
import os
from flask import Flask, render_template, url_for, request, session, redirect, flash, abort

app = Flask(__name__)
menu = ["Download", "First app", "Contact us"]
secret_key = 'The most secret key ever'
app.config['SECRET_KEY'] = secret_key

# vars for html
success = 'alert-success'
error = 'alert-danger'


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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title="Page not found"), 404


if __name__ == "__main__":
    app.run(debug=True)
