import sqlite3

def all_stories():
    db = sqlite3.connect("data/data.db")
    c = db.cursor()

    c.execute("SELECT * FROM stories")
    returnList = c.fetchall()
    db.close()
    return returnList

def search( whatLook ):
    db = sqlite3.connect("data/data.db")
    c = db.cursor()

    c.execute("SELECT * FROM stories")
    whatSearch = c.fetchall()
    results = []
    for tup in whatSearch:
        if whatLook in tup[1] or whatLook in tup[2]:
            results.add(tup)
    return results
