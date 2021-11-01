import sqlite3

def checkKey(dict, key):
      
    if key in dict.keys():
        value = True
    else:
        value = False
    return value

def createTable(con,cur, gameRoundData, gameID):
    mapID = gameRoundData["map"]

    detectionData = gameRoundData["room_detection_prob"]

    for i in range(len(detectionData)):
        roomdet = detectionData[i]
        cur.execute("""INSERT INTO Detection (gameID,mapID, room, probDet) \
            VALUES (?, ?, ?,  ?)""", (gameID, mapID, i+1, roomdet))
        con.commit()