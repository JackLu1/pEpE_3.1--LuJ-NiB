import sqlite3

def all_stories():
    db = sqlite3.connect("../data/data.db")
    c = db.cursor()

    c.execute("SELECT * FROM stories")
    return c.fetchall()

def search( whatLook ):
    
