__author__ = 'Kyle Dumouchelle'
# CPSC409, 11/30/2015

import sqlite3
from config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:

    # get cursor for SQL execution
    c = connection.cursor()

    # create table
    c.execute("DROP TABLE IF EXISTS tasks")
    c.execute("""CREATE TABLE tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTEGER NOT NULL,
    status INTEGER NOT NULL)""")

    # insert dummy data
    c.execute("""INSERT INTO tasks (name, due_date, priority, status)
              VALUES("Finish this tutorial", "12/04/2015", 10, 1)""")
    c.execute("""INSERT INTO tasks (name, due_date, priority, status)
              VALUES("Finish this assignment", "12/04/2015", 10, 1)""")