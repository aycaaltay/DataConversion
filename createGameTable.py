import sqlite3

def checkKey(dict, key):
      
    if key in dict.keys():
        value = dict[key]
    else:
        value =0 
    return value

def get_value(dct, substring):
    for key, val in dct.items():
        if isinstance(key, str) and substring in key:
            yield val
        elif isinstance(val, dict):
            yield from get_value(val, substring)

def createTable(con,cur, gameRoundData, gameTimeIndicator, gameID):

	writeRound = 0

	gameIdentifier = checkKey(gameRoundData, "game_identifier")

	if gameIdentifier ==0:
		gameIdentifier = None

	computerID = checkKey(gameRoundData, 'player_identifier')
	if computerID == 0:
		computerID = checkKey(gameRoundData, 'identifier')

	nickname = gameRoundData['nickname']

	mapID = gameRoundData["map"]

	RoundScore = gameRoundData["single_round_score"]

	role = gameRoundData["player_role"]

	totalScore = gameRoundData["total_score"]

	level = gameRoundData["game speed level"]

	speed = gameRoundData["game speed"]

	bomb_information = checkKey(gameRoundData, 'bomb_information')

	is_bomb_dropped = None
	timeBombDrop = None
	locationBomb = None
	bombXCoor = None
	bombYCoor = None
	bombCaught = None
	is_bomb_exploded = None
	timeBombExplode = None
	timeBombCaught = None
	whichPatrollerBomb = None
	gameResultCategory = None
	playerEscaped = None
	playerMarked = None
	playerCaught = None
	attackerCaught = None
	whichPatrollerAttacker = None
	isFinal = None
	gameRoundNumber = None
	
	if bomb_information !=0:
		is_bomb_dropped = bomb_information["is_bomb_dropped"]
		if is_bomb_dropped == True:
			locationBomb = bomb_information["bomb_location"][0]
			bombXCoor = bomb_information["bomb_location"][1][0]
			bombYCoor = bomb_information["bomb_location"][1][1]
			if is_bomb_dropped == True:
				is_bomb_exploded = bomb_information["is_bomb_explode"]
				if is_bomb_exploded == True:
					timeBombExplode = bomb_information["explosion_time"]

	elif checkKey(gameRoundData, "game_result") !=0:
		isFinal = gameRoundData["is_game_final"]
		gameRoundNumber = gameRoundData["game_round"]
		gameResult = gameRoundData["game_result"]
		bomb_information = gameResult["paintball_summary"]
		is_bomb_dropped = bomb_information["is_paintball_dropped"]
		timeBombDrop = bomb_information["paintball_drop_time"]
		locationBomb = bomb_information["paintball_location"][0]
		bombXCoor = bomb_information["paintball_location"][1][0]
		bombYCoor = bomb_information["paintball_location"][1][1]
		bombCaught = bomb_information["is_paintball_caught"]
		is_bomb_exploded = bomb_information["is_paintball_splash"]
		timeBombExplode = bomb_information["paintball_splash_time"]
		bombCaught = bomb_information["is_paintball_caught"]
		timeBombCaught = bomb_information["paintball_caught_time"]
		gameResultCategory = gameResult["game result category"]
		patrollers = gameResult["patroller_summary"]

		if timeBombCaught != None:
			patrollers = gameResult["patroller_summary"]
			if patrollers["patroller1"]["is_catch_bomb"] == True:
				whichPatrollerBomb = 1
			elif patrollers["patroller2"]["is_catch_bomb"] == True:
				whichPatrollerBomb = 2
		if role == "Attacker":
			playerInfo = gameResult["player_summary"]
			playerEscaped = playerInfo["is_player_escaped"]
			playerMarked = playerInfo["is_player_marked"]
			playerCaught = playerInfo["is_player_caught"]
			if playerCaught == True:
				patrollers = gameResult["patroller_summary"]
				if patrollers["patroller1"]["is_catch_attacker"] == True:
					whichPatrollerBomb = 1
				elif patrollers["patroller2"]["is_catch_attacker"] == True:
					whichPatrollerBomb = 2
		if role == "Patroller":
			gameResultCategory = gameRoundData["game_result"]["game result category"]
			gameRoundNumber = gameRoundData["game_round"]
			playerInfo = gameRoundData["game_result"]["player_summary"]
			playerMarked = playerInfo["is_player_marked"]
			isFinal = gameRoundData["is_game_final"]
			bomb_information = gameRoundData["game_result"]["paintball_summary"]
			is_bomb_dropped = bomb_information["is_paintball_dropped"]
			timeBombDrop = bomb_information["paintball_drop_time"]
			locationBomb = bomb_information["paintball_location"][0]
			bombXCoor = bomb_information["paintball_location"][1][0]
			bombYCoor = bomb_information["paintball_location"][1][1]
			is_bomb_exploded = bomb_information["is_paintball_splash"]
			timeBombExplode = bomb_information["paintball_splash_time"]
			bombCaught = bomb_information["is_paintball_caught"]
			timeBombCaught = bomb_information["paintball_caught_time"]
			attackerData = gameRoundData["game_result"]["AI_attacker_summary"]
			attackerCaught = attackerData["is_AI_attacker_caught"]
			playerEscaped = attackerData["is_AI_attacker_escaped"]
			playerMarked = attackerData["is_AI_attacker_marked"]
			if bombCaught == True:
				if gameRoundData["game_result"]["patroller_summary"]["patroller1"]["is_catch_bomb"]:
					whichPatrollerBomb = 1
				elif gameRoundData["game_result"]["patroller_summary"]["patroller2"]["is_catch_bomb"]:
					whichPatrollerBomb = 2
				else: 
					whichPatrollerBomb = 3
			if attackerCaught == True:
				if gameRoundData["game_result"]["patroller_summary"]["patroller1"]["is_catch_attacker"]:
					whichPatrollerAttacker = 1
				elif gameRoundData["game_result"]["patroller_summary"]["patroller2"]["is_catch_attacker"]:
					whichPatrollerAttacker = 2
				else: 
					whichPatrollerAttacker = 3

		if isFinal == None:
			isFinal = False

	
	

	cur.execute("""INSERT INTO Game (gameID, gameTimeIndicator, gameNumber, computerID, nickname, mapID, \
		playerRole, level, speed, planted, timeBombDrop, locationBomb, bombXCoor, bombYCoor, \
		playerEscaped, playerMarked, bombCaught, whichPatrollerBomb, exploded, timeBombExplode, \
		attackerCaught, whichPatrollerAttacker, timeBombCaught, isFinal, roundScore, totalScore, \
		gameResCat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
		?, ?, ?, ?, ?)""", (gameID, gameTimeIndicator, gameIdentifier, computerID, nickname, mapID, role, level, speed, \
			is_bomb_dropped, timeBombDrop, locationBomb, bombXCoor, bombYCoor, playerEscaped, playerMarked, \
			bombCaught, whichPatrollerBomb, is_bomb_exploded, timeBombExplode, attackerCaught, \
			whichPatrollerAttacker, timeBombCaught, isFinal, RoundScore, totalScore, gameResultCategory))
	con.commit()



		