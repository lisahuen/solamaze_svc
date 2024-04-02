from urllib.parse import quote
import mysql.connector
import json
from flask import Flask, make_response


with open('./config.json', 'r') as f:
    config_data = json.load(f)

def connectDatabaseMysqlConnector():
    try:

        server = config_data["Common"]["ServerInfo"]["Server"]
        user =  config_data["Common"]["ServerInfo"]["User"]
        pw = config_data["Common"]["ServerInfo"]["Pwd"]
        dbname = config_data["Common"]["ServerInfo"]["DBList"]
        portno = config_data["Common"]["ServerInfo"]["PortNo"]

        return mysql.connector.connect(host=server, user=user, passwd=pw, db=dbname, port = portno)


    except Exception as e:
        print(e)
        raise ValueError("error in connect to db")

def getTransByID(maze_id, tran_id):
#     maze_id = 'c8472ce9de0647529b2853778cfda6f8'
#     tran_id= 24
    mSQL = "select move_addr, move_sgn, move_direction, success_move, goal, svg_image  " \
           "from maze_transaction where maze_id = '%s'  and tran_id=%s;" % (maze_id,tran_id)

    with connectDatabaseMysqlConnector() as dbConnect:
        cursor = dbConnect.cursor()
        cursor.execute(mSQL)
        row = cursor.fetchone()
    if row:
        result = {'move_addr': row[0], 'move_sgn': row[1], 'move_direction':row[2],
                  'success_move':row[3],'goal':row[4],'svg_image':row[5]}
        json_data = json.dumps(result)
        return json_data
    else:
        return make_response('')



def getStartDisplayTransID():

    mSQL = 'select maze_id, max(tran_id) as tran_id from maze_transaction where maze_id in (select maze_id From maze_master where status=1) group by maze_id;'
    with connectDatabaseMysqlConnector() as dbConnect:
        cursor = dbConnect.cursor()
        cursor.execute(mSQL)
        row = cursor.fetchone()

    if row:
        result = {'maze_id': row[0], 'tran_id': row[1]}
        json_data = json.dumps(result)
        return json_data
    else:
        return make_response('')


def getWinHistory():

    mSQL = 'select maze_id, finish_dt, move, winner_addr, winner_sgn From maze_master  where status in (0,2) and finish_dt is not null  order by finish_dt desc limit 10;'
    with connectDatabaseMysqlConnector() as dbConnect:
        cursor = dbConnect.cursor()
        cursor.execute(mSQL)
        rows = cursor.fetchall()

    results = []
    for row in rows:
        result = {'maze_id': row[0], 'finish_dt': str(row[1]), 'move':row[2],'winner_addr': row[3], 'winner_sgn': row[4]}
        results.append(result)

    # Convert results to JSON format
    json_data = json.dumps(results)

    return json_data

