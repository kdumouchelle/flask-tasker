__author__ = 'Kyle Dumouchelle'
# CPSC409, 12/04/2015

# controller

import sqlite3
from functools import wraps
from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
from forms import AddTaskForm

# configuration (remote)
app = Flask(__name__)
app.config.from_object("config")

# function used for connecting to databse
def connnect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Login Required')
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
            flash('Logged In')
            return redirect(url_for('tasks'))
    return render_template('login.html', error=error)

@app.route('/tasks')
@login_required
def tasks():
    g.db = connnect_db()
    cur = g.db.execute('SELECT name, due_date, priority, task_id FROM tasks WHERE status=1')
    open = [dict(name=row[0], due_date=row[1],priority=row[2], task_id=row[3])
            for row in cur.fetchall()]
    cur = g.db.execute('SELECT name, due_date, priority, task_id FROM tasks WHERE status=0')
    closed = [dict(name=row[0], due_date=row[1],priority=row[2], task_id=row[3])
            for row in cur.fetchall()]
    g.db.close()
    return render_template(
        'tasks.html',form=AddTaskForm(request.form),
        open_tasks=open, closed_tasks=closed)

@app.route('/add', methods=['POST'])
@login_required
def add_task():
    name = request.form['name']
    date = request.form['due_date']
    priority = request.form['priority']

    if not name or not date or not priority:
        flash("Fill out all fields and try again.")
        return redirect(url_for('tasks'))

    else:
        g.db = connnect_db()
        g.db.execute('INSERT INTO tasks (name, due_date, priority, status) '
                     'VALUES (?, ?, ?, 1)',
                     [name, date, priority])
        g.db.commit()
        g.db.close()
        flash('New task posted')
        return redirect(url_for('tasks'))

# Marks task complete
@app.route('/complete/<int:task_id>')
@login_required
def complete(task_id):
    g.db = connnect_db()
    g.db.execute('UPDATE tasks SET status = 0 WHERE task_id='+str(task_id))
    g.db.commit()
    g.db.close()
    flash('Task marked as complete')
    return redirect(url_for('tasks'))

# Delete task
@app.route('/delete/<int:task_id>')
@login_required
def delete_entry(task_id):
    g.db = connnect_db()
    g.db.execute('DELETE FROM tasks WHERE task_id='+str(task_id))
    g.db.commit()
    g.db.close()
    flash('Task deleted')
    return redirect(url_for('tasks'))

@app.route('/logout')
def logout():
    # returns session key to default and returns to login page
    session.pop('logged_in', None)
    flash('Logged Out')
    return redirect(url_for('login'))