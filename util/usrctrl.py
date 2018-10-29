'''This file performs database functions for user info'''
import sqlite3

path = "data/data.db"

# def check_session(session):
#     '''checks if user in session, avoid crash when returning to page after logout'''

def login_check(check_usr, check_pw):
    '''searches database for user matching username'''
    db = sqlite3.connect(path)
    c = db.cursor()
    c.execute("SELECT name, pw FROM users")
    # list of tuples
    info = c.fetchall()
    # i is tuple in format (user, pw)
    db.close()
    for i in info:
        if check_usr == i[0] and check_pw == i[1]:
            return True
    return False

def new_user(usr, pw):
    '''Adds new user to database'''
    db = sqlite3.connect(path)
    c = db.cursor()

    c.execute("SELECT userid FROM users")
    info = c.fetchall()

    # userid is len(info)
    params = (len(info), usr, pw)
    c.execute("INSERT INTO users VALUES(?, ?, ?)", params)

    db.commit()
    db.close()


