from maze_main import Maze
import random
import time
import datetime
import general
import uuid
import transaction

import os
import string

def job_start():

    goal = 1
    while 1==1:
        if goal == 1:
            maze, uuid = maze_generate()
            tran_id=2
            goal = 0
        else:
            while not goal:
                print(tran_id)
                goal = maze_run(maze, uuid,tran_id)
                tran_id += 1

            print("completed maze: %s" % uuid)

def maze_generate():

    nx, ny = 2 , 2
    # # Maze entry position
    ix, iy = 0, 0
    cx, cy = 0, 0
    filename = 'img0.svg'
    #
    maze = Maze(nx, ny, cx, cy, ix, iy)
    maze.add_begin_end = True
    maze.add_treasure = False
    maze.make_maze()
    maze.write_svg(filename)

    mCurrentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open('./'+filename, 'r') as f:
        svg_content = f.read()

    clear_table()

    mUUID = uuid.uuid4().hex
    #
    mSQL1 = "insert into maze_master(maze_id, create_dt, status) values('%s','%s',1);" % (mUUID, mCurrentTime)
    mSQL2 = "insert into maze_transaction" \
            "(maze_id, tran_id, move_addr, move_sgn, move_direction, success_move, goal, create_dt, svg_image) " \
            "values('%s',1,'','','X', 2,2,'%s','%s');" \
            % (mUUID, mCurrentTime, svg_content)
    #
    with general.connectDatabaseMysqlConnector() as dbConnect:
        cursor = dbConnect.cursor()
        cursor.execute(mSQL1)
        cursor.execute(mSQL2)
        dbConnect.commit()
    #
    return (maze, mUUID)

    # call maze_run(maze, mUUID)


def distribute_character(character):
    if not isinstance(character, str) or len(character) != 1 or not character.isalnum():
        raise ValueError("Input must be a single alphanumeric character.")

    mapping = {
        "0": "N",
        "1": "S",
        "2": "E",
        "3": "W",
        "4": "N",
        "5": "S",
        "6": "E",
        "7": "W",
        "8": "N",
        "9": "S",
        "A": "E",
        "B": "W",
        "C": "N",
        "D": "S",
        "E": "E",
        "F": "W",
        "G": "N",
        "H": "S",
        "I": "E",
        "J": "W",
        "K": "N",
        "L": "S",
        "M": "E",
        "N": "W",
        "O": "N",
        "P": "S",
        "Q": "E",
        "R": "W",
        "S": "N",
        "T": "S",
        "U": "E",
        "V": "W",
        "W": "N",
        "X": "S",
        "Y": "E",
        "Z": "W",
        "a": "N",
        "b": "S",
        "c": "E",
        "d": "W",
        "e": "N",
        "f": "S",
        "g": "E",
        "h": "W",
        "i": "N",
        "j": "S",
        "k": "E",
        "l": "W",
        "m": "N",
        "n": "S",
        "o": "E",
        "p": "W",
        "q": "N",
        "r": "S",
        "s": "E",
        "t": "W",
        "u": "N",
        "v": "S",
        "w": "E",
        "x": "W",
        "y": "N",
        "z": "S",
    }

    direction = mapping.get(character, None)

    if direction is None:
        raise ValueError("No mapping found for the input character.")

    return direction

def direction_gen():

    hash_now, move_sgn, move_addr = transaction.get_latest_transaction()

    directions = distribute_character(move_sgn[-3])
    return directions, move_addr, move_sgn

def maze_run(maze, uuid, tran_id):

    # time.sleep(0.5)

    direction, move_addr, move_sgn = direction_gen()

    success_move, goal = maze.update_maze(direction)
    filename = 'img.svg'
    maze.write_svg(filename)

    with open('./'+filename, 'r') as f:
        svg_content = f.read()

    mCurrentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mSQL2 = "insert into maze_transaction" \
            "(maze_id, tran_id, move_direction, move_addr, move_sgn, success_move, goal, create_dt, svg_image) " \
            "values('%s','%s','%s','%s','%s',%s,%s,'%s','%s');" \
            % (uuid, tran_id, direction, move_addr, move_sgn, success_move,goal, mCurrentTime, svg_content)

    with general.connectDatabaseMysqlConnector() as dbConnect:
        cursor = dbConnect.cursor()
        cursor.execute(mSQL2)
        dbConnect.commit()


    if goal:
        mCurrentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        mPrizeTransaction = transaction.transfer_token(move_addr)
        print(mPrizeTransaction)
        # time.sleep(5)
        # mPrizeTransaction = ''

        mSQL3 = "update maze_master set status=0 where status=2;"
        mSQL5 = "update maze_master set status=2, move=%s, finish_dt='%s', " \
                "winner_addr = '%s', winner_sgn = '%s', prize_txn='%s' " \
                "where maze_id = '%s';" \
                % (tran_id, mCurrentTime,move_addr, move_sgn, mPrizeTransaction, uuid)

        with general.connectDatabaseMysqlConnector() as dbConnect:
            cursor = dbConnect.cursor()
            cursor.execute(mSQL3)
            cursor.execute(mSQL5)
            dbConnect.commit()

        clear_table()

    return goal

def clear_table():
    # mSQL3 = "update maze_master set status=0 where status=2;"
    mSQL4 = "update maze_master set status=2 where status=1;"
    mSQL6 = "delete From maze_transaction a where maze_id in " \
            "(select maze_id from maze_master b where a.maze_id =b.maze_id and b.status=0);"

    with general.connectDatabaseMysqlConnector() as dbConnect:
        cursor = dbConnect.cursor()
        # cursor.execute(mSQL3)
        cursor.execute(mSQL4)
        cursor.execute(mSQL6)
        dbConnect.commit()