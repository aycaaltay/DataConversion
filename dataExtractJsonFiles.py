# Python program to read json file
import json
import sqlite3
import pandas as pd
import numpy as np
from collections import Counter

import generateTable
import oneTimeRuns
import gameDataProcessing
import keyRetrieval
import createUsersTable
import createGameTable
import createMovementTable
import createPopulationTable
import createDetectionTable

def checkKey(dict, key):
      
    if key in dict.keys():
        value = dict[key]
    else:
        value =0 
    return value

def build_matrix(rows, cols):
    matrix = []

    for r in range(0, rows):
        matrix.append([0 for c in range(0, cols)])

    return matrix

#Does the db file exist?
def isSQLite3(filename):
    from os.path import isfile, getsize

    if not isfile(filename):
        return False
    if getsize(filename) < 100: 
    # SQLite database file header is 100 bytes.
    # A db file is very unlikely to be smaller
        return False
    if isfile(filename) and getsize(filename) >= 100:
        return True

fileName = 'GameData.db'

#Check if the database file exists
fileExists = isSQLite3(fileName)

if fileExists:
    print('\nThe database file exists. Only new data will be entered.\n')
else:
    print("\nThe database file does not exist. It will be created.\n")

#If the file doesn't exists, than do the one-time tasks.
# These tasks involve database creation, map information
# loading, etc. 
if fileExists == False:
    oneTimeRuns.oneTimeRuns(fileName)



# Opening JSON file
f = open('game-records.json',)
 
# returns JSON object as a dictionary
data = json.load(f)
size1 =len(data)
print(size1,"data points are available.\n")
keys = data.keys()

con = sqlite3.connect(fileName) # change to 'sqlite:///your_filename.db'
# drop data into database
cur = con.cursor()


keyList = []
#For every record
for key in keys:

    keyList.append(keyRetrieval.accumulate_keys(data[key]))


#Find all data sstructures in the json file    
mylist =  [x for i, x in enumerate(keyList) if i == keyList.index(x)]
counts = [0]*len(mylist)
a=0
for i in mylist:
    counts[a] = sum(x.count(i) for x in enumerate(keyList))
    a+=1

print("There are", str(a), "different structures.")



# If a data structure has less than 20 games, then don't count
a=0
theList = []
for i in mylist: 
    if counts[a] > 30:
        theList.append(i) 
    a+=1

print(str(len(theList)), "of them have enough data to be processed.\n")


for key in keys:
    gameTimeIndicator = key[len(key)-20:]
    gameTimeIndicator = gameTimeIndicator.replace("-","")
    gameTimeIndicator = gameTimeIndicator.replace("[","")
    gameTimeIndicator = gameTimeIndicator.replace("]","")
    gameTimeIndicator = gameTimeIndicator.replace("'","")
    
    checkRecord = cur.execute("""SELECT COUNT(gameTimeIndicator) FROM Game WHERE gameTimeIndicator = ?;""", (gameTimeIndicator,))
    results = checkRecord.fetchall()

    specificKey = keyRetrieval.accumulate_keys(data[key])    

    validRound = specificKey in theList

    #If the game record doesn't exist and the keys are in the allowed keys list
    if results[0][0]==0 and validRound:
        gameRoundData = data[key]

        noRec = cur.execute("""SELECT COUNT(*) FROM Game""")
        noR = noRec.fetchall()
        
        if noR[0][0] == 0:
            gameID =1 
        else:
            checkRecord = cur.execute("""SELECT max(gameID) FROM Game""")
            gameID = checkRecord.fetchall()
            gameID =gameID[0][0] + 1

        createUsersTable.createTable(con, cur, gameRoundData)

        createGameTable.createTable(con,cur, gameRoundData, gameTimeIndicator, gameID)

        createMovementTable.createTable(con,cur, gameRoundData,gameID)

        createPopulationTable.createTable(con,cur, gameRoundData,gameID)
        createDetectionTable.createTable(con,cur, gameRoundData,gameID)



        


        
    





            

con.close()



# Closing file
f.close()