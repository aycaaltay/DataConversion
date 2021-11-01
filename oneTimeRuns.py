import pandas as pd
import csv
import sqlite3
import generateTable
    

def oneTimeRuns(fileName):

    generateTable.generateTableMethod()
    # load data
    df = pd.read_csv('Maps.csv')

    # strip whitespace from headers
    df.columns = df.columns.str.strip()
    df = df.apply(pd.to_numeric)

    con = sqlite3.connect(fileName) # change to 'sqlite:///your_filename.db'


    # drop data into database
    cur = con.cursor()
    query1 = cur.execute("""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Maps' ;""")
    #e = cur.fetchone().[0]
    #res = functools.reduce(lambda sub, ele: sub * 10 + ele, e)

    #cur.execute("ALTER TABLE Maps MODIFY COLUMN mapID TYPE integer;")

    #print(res, res ==0)

    if cur.fetchone()[0] == 0:
        df.to_sql("Maps", con)
        con.commit()
    else:
        query = cur.execute("""SELECT COUNT(*) FROM Maps;""")
        if query is None: 
            cur.execute("""DROP TABLE Maps;""")
            df.to_sql("Maps", con)
            cur.execute("""ALTER TABLE Maps DROP COLUMN Index;""")
            cur.execute("""ALTER TABLE Maps ADD PRIMARY KEY (mapID);""")
            cur.execute("""ALTER TABLE Maps ADD FOREIGN KEY (mapID) REFERENCES Game(mapID);""")
            con.commit()


    df = pd.read_csv('Categories.csv')
    df.columns = df.columns.str.strip()
    cur = con.cursor()
    query1 = cur.execute("""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='GameResultCategories' ;""")
    #e = cur.fetchone().[0]
    #res = functools.reduce(lambda sub, ele: sub * 10 + ele, e)

    #cur.execute("ALTER TABLE Maps MODIFY COLUMN mapID TYPE integer;")

    #print(res, res ==0)

    
    df.to_sql("GameResultCategories", con)
    #cur.execute("""ALTER TABLE GameResultCategories DROP COLUMN index;""")
    #cur.execute("""ALTER TABLE GameResultCategories ADD PRIMARY KEY (role, gameResCat);""")
    #cur.execute("""ALTER TABLE GameResultCategories ADD FOREIGN KEY (gameResCat) REFERENCES Game(gameResCat);""")

    con.commit()

    con.close()


    