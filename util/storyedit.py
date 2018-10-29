import sqlite3

def edit(sID, addition):
    '''this adds a new portion of the story to the story with story ID sID'''
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

    material = (sID, title, addition, max + 1, 0) # make sure 0 will be replaced with userid (get from users / signed in acc)

    c.execute("INSERT INTO stories VALUES(?, ?, ?, ?, ?)", material)
    db.commit()
    db.close()

def add(addition, title):
    '''this adds a completely new story with title title'''
    db = sqlite3.connect("data/data.db")
    c = db.cursor()
    c.execute("SELECT * FROM stories")
    al = c.fetchall()
    mx = 0
    emx = 0
    for tup in al:
        if tup[0] > mx:
            mx = tup[0]

        if tup[3] > emx:
            emx = tup[3]

    material = (mx + 1, title, addition, emx + 1, 0) # make sure 0 will be replaced with userid (get from users / signed in acc)

    c.execute("INSERT INTO stories VALUES(?, ?, ?, ?, ?)", material)
    db.commit()
    db.close()
