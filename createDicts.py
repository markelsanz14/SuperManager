import sqlite3
import getpass


def createDicts(): 
    connection = sqlite3.connect('supermanager.db')
    try:
        cursor = connection.cursor()
        query = "SELECT DISTINCT player FROM Players;"
        cursor.execute(query)
        values = cursor.fetchall()

        # Create dictionary to transform from name to number
        names_dict = {}
        i = 0
        for name in values:
            names_dict[name[0]] = i
            i += 1


        query = "SELECT DISTINCT team FROM Players;"
        cursor.execute(query)
        values = cursor.fetchall()

        # Create dictionary to transform from team to number
        teams_dict = {}
        i = 0
        for team in values:
            teams_dict[team[0]] = i
            i += 1

    finally:
        connection.close()
        print("DICTIONARIES READ")
    return names_dict, teams_dict

