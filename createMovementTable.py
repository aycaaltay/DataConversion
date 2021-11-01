import sqlite3

def checkKey(dict, key):
      
    if key in dict.keys():
        value = True
    else:
        value = False
    return value

def createTable(con,cur, gameRoundData, gameID):
    role = gameRoundData["player_role"]
    track = gameRoundData["player_track"]
    mapID = gameRoundData["map"]

    if checkKey(gameRoundData, "policemen_track") == True:
        patroller1 = gameRoundData["policemen_track"]["policeman1"]
        if checkKey(gameRoundData["policemen_track"], "policeman2") == True:
            patroller2 = gameRoundData["policemen_track"]["policeman2"]
    elif checkKey(gameRoundData, "patroller_track") == True:
        patroller1 = gameRoundData["patroller_track"]["patroller1"]
        if checkKey(gameRoundData["patroller_track"], "patroller2") == True:
            patroller2 = gameRoundData["patroller_track"]["patroller2"]
    else:
        print("This is a new data type. I cannot record this game\n\n\n")

    instants = len(gameRoundData["player_track"])

    for j in range(instants):
        room1 = patroller1[j][0]
        xcoor1 = patroller1[j][1][0]
        ycoor1 = patroller1[j][1][1]      
        cur.execute("""INSERT INTO Movement (gameID,mapID, agent, instant, room, XCoor, YCoor) \
            VALUES (?, ?, ?, ?, ?, ?, ?)""", (gameID, mapID, "Patroller1", j+1, room1, xcoor1, ycoor1))
        con.commit()
        if 'patroller2' in locals():
            room2 = patroller2[j][0]
            xcoor2 = patroller2[j][1][0]
            ycoor2 = patroller2[j][1][1]      
            cur.execute("""INSERT INTO Movement (gameID,mapID, agent, instant, room, XCoor, YCoor) \
                VALUES (?, ?, ?, ?, ?, ?, ?)""", (gameID, mapID, "Patroller2", j+1, room2, xcoor2, ycoor2))
            con.commit()
    
    if role == "Attacker":
        for j in range(instants):
            room = track[j][0]
            xcoor = track[j][1][0]
            ycoor = track[j][1][1]      
            cur.execute("""INSERT INTO Movement (gameID,mapID, agent, instant, room, XCoor, YCoor) \
                VALUES (?, ?, ?, ?, ?, ?, ?)""", (gameID, mapID, role, j+1, room, xcoor, ycoor))
            con.commit()

    else:
        for j in range(instants):
            room = track[j][0]
            xcoor = track[j][1][0]
            ycoor = track[j][1][1]      
            cur.execute("""INSERT INTO Movement (gameID,mapID, agent, instant, room, XCoor, YCoor) \
                VALUES (?, ?, ?, ?, ?, ?, ?)""", (gameID, mapID, "Patroller", j+1, room, xcoor, ycoor))
            con.commit()
        if checkKey(gameRoundData, "game_result"):
            if len(gameRoundData["AI_attacker_track"]) >0: 
                attacker = gameRoundData["AI_attacker_track"]
                if len(gameRoundData["AI_attacker_track"]) == instants:
                    
                    for j in range(instants):
                        room = attacker[j][0]
                        xcoor = attacker[j][1][0]
                        ycoor = attacker[j][1][1]      
                        cur.execute("""INSERT INTO Movement (gameID,mapID, agent, instant, room, XCoor, YCoor) \
                            VALUES (?, ?, ?, ?, ?, ?, ?)""", (gameID, mapID, "Attacker", j+1, room, xcoor, ycoor))
                        con.commit()
                else:
                    attacker = gameRoundData["AI_attacker_track"]
                    for j in range(instants-len(gameRoundData["AI_attacker_track"])):
                        room = attacker[j][0]
                        xcoor = attacker[j][1][0]
                        ycoor = attacker[j][1][1]      
                        cur.execute("""INSERT INTO Movement (gameID,mapID, agent, instant, room, XCoor, YCoor) \
                            VALUES (?, ?, ?, ?, ?, ?, ?)""", (gameID, mapID, "Attacker", \
                                j+1+instants-len(gameRoundData["AI_attacker_track"]), room, xcoor, ycoor))
                        con.commit()






