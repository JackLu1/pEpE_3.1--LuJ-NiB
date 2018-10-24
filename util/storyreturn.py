import sqlite3

def all_stories():
    db = sqlite3.connect("data/data.db")
    c = db.cursor()

    c.execute("SELECT * FROM stories")
    returnList = c.fetchall()
    
    db.close()
    
    returnList = removeOverlap(returnList)

    return returnList

def search( whatLook ):
    db = sqlite3.connect("data/data.db")
    c = db.cursor()

    c.execute("SELECT * FROM stories")
    whatSearch = c.fetchall()
    results = []
    for tup in whatSearch:
        if whatLook in tup[1] or whatLook in tup[2]:
            results.append(tup)
    db.close()

    results = removeOverlap(results)

    return results

def removeOverlap( stories ):
    overlaps = {}

    for tup in stories:
        if tup[0] not in overlaps.keys():
            overlaps[tup[0]] = tup
        else:
            if tup[3] > overlaps[tup[0]][3]:
                overlaps[tup[0]] = tup

    returnList = list(overlaps.values())
    return returnList

def get( sID ):
    db = sqlite3.connect("data/data.db")
    c = db.cursor()

    c.execute("SELECT * FROM stories")
    whatSearch = c.fetchall()
    results = [sID, None, None, 0]
    for tup in whatSearch:
        if sID == tup[0] and tup[3] >= results[3]:
            results[1] = tup[1]
            results[2] = tup[2]
            results[3] = tup[3]
    db.close()
    return results
