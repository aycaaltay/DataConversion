import sqlite3
from sqlite3 import Error

def generateTableMethod():

	conn    = sqlite3.connect("GameData.db")


	cursorObject = conn.cursor()
	createTable = "CREATE TABLE IF NOT EXISTS Users(computerID varchar(100), nickname varchar(32), \
	PRIMARY KEY(computerID, nickname) \
    FOREIGN KEY(nickname) REFERENCES Game(nickname) ON DELETE SET DEFAULT ON UPDATE SET DEFAULT \
    FOREIGN KEY(computerID) REFERENCES Game(computerID) ON DELETE SET DEFAULT ON UPDATE SET DEFAULT)"
	cursorObject.execute(createTable)

	createTable = "CREATE TABLE IF NOT EXISTS Game(gameID int PRIMARY KEY , gameTimeIndicator varchar(40), gameNumber varchar(200), computerID varchar(40), \
	nickname varchar(40), mapID  int, playerRole varchar(20), level varchar(10), speed int, \
	planted boolean, timeBombDrop int, locationBomb int, bombXCoor int, bombYCoor int, \
	playerEscaped boolean, playerMarked boolean, \
	bombCaught boolean, whichPatrollerBomb int,	exploded boolean, timeBombExplode int, \
	attackerCaught boolean, whichPatrollerAttacker int, timeBombCaught int, \
	isFinal boolean, roundScore int, totalScore int, gameResCat int, \
	FOREIGN KEY(gameID) REFERENCES Detection(gameID) ON DELETE SET DEFAULT ON UPDATE SET DEFAULT \
    FOREIGN KEY(mapID) REFERENCES Maps(mapID) ON DELETE SET DEFAULT ON UPDATE SET DEFAULT \
    FOREIGN KEY(gameID) REFERENCES Movement(gameID) ON DELETE SET DEFAULT ON UPDATE SET DEFAULT \
    FOREIGN KEY(gameID) REFERENCES Population(gameId) ON DELETE SET DEFAULT ON UPDATE SET DEFAULT )"
	cursorObject.execute(createTable)

	#createTable = "CREATE TABLE IF NOT EXISTS Maps(mapId int, room int, centrality int, \
	#centralityRank int)"
	#cursorObject.execute(createTable)

	createTable = "CREATE TABLE IF NOT EXISTS Detection(gameID int, mapID int, \
	room int, probDet float, PRIMARY KEY(gameID, room) FOREIGN KEY(gameID) REFERENCES Game(gameID) \
    ON DELETE SET DEFAULT ON UPDATE SET DEFAULT);"
	cursorObject.execute(createTable)


	createTable = "CREATE TABLE IF NOT EXISTS Movement(gameID int, mapID int, agent varchar(20), instant int,\
	room int, xCoor int, yCoor int, PRIMARY KEY(gameID, mapID, agent, instant) FOREIGN KEY(gameID) REFERENCES Game(gameID) \
    ON DELETE SET DEFAULT ON UPDATE SET DEFAULT)"
	cursorObject.execute(createTable)

	createTable = "CREATE TABLE IF NOT EXISTS Population(gameId int, mapID int, room int, instant int, \
	population int, PRIMARY KEY(gameId, room, instant) FOREIGN KEY(gameId) REFERENCES Game(gameID) \
    ON DELETE SET DEFAULT ON UPDATE SET DEFAULT \
    FOREIGN KEY(mapID) REFERENCES Maps(mapID) ON DELETE SET DEFAULT ON UPDATE SET DEFAULT\
    FOREIGN KEY(gameID, instant) REFERENCES Movement(gameID, instant) ON DELETE SET DEFAULT ON UPDATE SET DEFAULT)"
	cursorObject.execute(createTable)

	createTable = "CREATE TABLE IF NOT EXISTS SimulationPoints(gameID int, mapID int, room int, xCoor int, \
	yCoor int, PRIMARY KEY(gameID, mapID, room, xCoor, yCoor) FOREIGN KEY (gameID) REFERENCES Game(gameID))"
	cursorObject.execute(createTable)

	createTable = "CREATE TABLE IF NOT EXISTS ReadFileNames(FileName varchar(200) PRIMARY KEY)"
	cursorObject.execute(createTable)

	print("\nTables are generated...")

	conn.close()



    

