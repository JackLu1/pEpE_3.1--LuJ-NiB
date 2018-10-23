import sqlite3

def edit(sID, addition):
    db = sqlite3.connect("data/data.db")
    c = db.cursor()
    c.execute("SELECT * FROM stories")
    all = c.fetchall()
    max = 0
    title = ""
    for tup in all:
        if tup[3] > max:
            max = tup[3]

        if sID == tup[0]:
            title = tup[1]

    material = (sID, title, addition, max + 1)

    c.execute("INSERT INTO stories VALUES(?, ?, ?, ?)", material)
    db.commit()
    db.close()
