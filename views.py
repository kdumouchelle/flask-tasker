__author__ = 'Kyle Dumouchelle'
#CPSC 409, 12/04/2015

#controller

import sqlite3
from functools import wraps
from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g

app = Flask(__name__)
#pulls in app configuration from config file
app.config.from_object("config")

#function used for connecting to databse
def connnect_db():
    return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
            request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Username and/or Password.'
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error = error)

@app.route('/main')
@login_required
def main():
    g.db = connnect_db()
    cur = g.db.execute('SELECT * FROM posts')
    posts = [dict(title=row[0], post=row[1])for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html', posts=posts)

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']

     #if either title or post are empty
    if not title or not post:
        flash("Fill out all fields and try again.")
        return redirect(url_for('main'))

    else:
        g.db = connnect_db()
        g.db.execute('INSERT INTO posts (title, post) VALUES (?, ?)',
                     [request.form['title'], request.form['post']])
        g.db.commit()
        g.db.close()
        flash('New entry posted')
        return redirect(url_for('main'))

@app.route('/logout')
def logout():
    #returns session key to default and returns to login page
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)