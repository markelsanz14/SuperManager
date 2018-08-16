import sqlite3
import getpass


def readDB(number):
    # Connect to the database
    connection = sqlite3.connect('supermanager.db')
    '''
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password=pw,
                                 db='supermanager',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    '''
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM Players WHERE season != 61 ORDER BY RANDOM() LIMIT " + str(number) + ";"
        cursor.execute(query)
        output = cursor.fetchall()


    finally:
        connection.close()

    return output
