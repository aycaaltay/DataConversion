import sqlite3

def checkKey(dict, key):
      
    if key in dict.keys():
        value = True
    else:
        value = False
    return value

def createTable(con,cur, gameRoundData, gameID):
    mapID = gameRoundData["map"]

    
    populationData = gameRoundData["room_occupancy_track"]
    instants = len(populationData)

    for i in range(instants):
        allRooms = populationData[i]
        for j in range(len(allRooms)):
            pop = allRooms[j]
            cur.execute("""INSERT INTO Population (gameID,mapID, room, instant, population) \
                VALUES (?, ?, ?, ?, ?)""", (gameID, mapID, j+1, i+1, pop))
            con.commit()