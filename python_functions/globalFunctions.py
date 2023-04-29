import baseDados as db

def getPlayers():
    res = db.getPlayers()
    for i in res:
        print(i)