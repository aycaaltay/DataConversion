
import sqlite3

def checkKey(dict, key):
      
    if key in dict.keys():
        value = dict[key]
    else:
        value =0 
    return value

def createTable(con, cur, gameRoundData):

	computerID = checkKey(gameRoundData, 'player_identifier')
	if computerID == 0:
		computerID = checkKey(gameRoundData, 'identifier')

	nickname = gameRoundData['nickname']
    #print(computerID, nickname)

    #Add computer ID and nickname 
	checkRecord = cur.execute("""SELECT COUNT(computerID) FROM Users \
    WHERE computerID = ? AND nickname = ?;""", (computerID, nickname,))
	results = checkRecord.fetchall()

    #If the computerID-nickname combination doesn't exist.
	if results[0][0]==0:
		cur.execute("""INSERT INTO Users (computerID, nickname) VALUES (?, ?)""", (computerID, nickname))
		con.commit()