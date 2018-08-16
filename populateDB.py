# coding: utf-8

# This file will fetch the list of players
import urllib
import sqlite3
from bs4 import BeautifulSoup


url_start = 'http://www.acb.com/fichas/LACB'
seasons = [57, 58, 59, 60, 61, 62] # 2012-13 to 2016-17
start_value = 1
end_values = [306, 306, 306, 306, 272, 18]


# Connect to the database
connection = sqlite3.connect('supermanager.db')
id_ = 1

try:
    cursor = connection.cursor()
    j = 0
    cursor.execute("CREATE TABLE Players (id int, player int, team int, rival int, season int, game int, val int)")
    for season in seasons:
        print("Reading season " + str(season))
        for i in range(start_value, end_values[j]+1):
            if i % 20 == 0:
                print("Reading game " + str(i))
            # Compose URL for each game
            if i < 10:
                url = url_start + str(season) + '00' + str(i) + '.php'
            elif i < 100:
                url = url_start + str(season) + '0' + str(i) + '.php'
            else:
                url = url_start + str(season) + str(i) + '.php'
            
            # Read url html
            sock = urllib.request.urlopen(url)
            html_doc = sock.read()

            # Parse html to get player info
            soup = BeautifulSoup(html_doc, 'html.parser')
            table = soup.findAll("table", "estadisticasnew")[1]
            tr_teams = table.findAll("tr", "estverde")
            tr = table.findAll("tr")

            # Read every row, and parse each case accordingly
            player_name = None
            team_names = []
            rivalTeam = None
            val = None
            # First find team names
            for row in tr_teams:
                cells = row.findAll("td")
                if len(cells) == 8: # team name found
                    name_list = cells[0].getText().split()[:-1]
                    name = ''
                    for n in name_list:
                        name += str(n) + ' '
                    name2 = name[:-1].replace("'", "")
                    team_names.append(name2)

            team_pos = -1
            other_pos = {0:1, 1:0}
            for row in tr:
                cells = row.findAll("td")
                if len(cells) == 8: # team name found
                    # Update team pos to correct pos in array
                    team_pos += 1
                else: # one row of the table
                    if cells[1].find("a") is not None and len(cells) != 2: # contains player name
                        player_n = cells[1].getText()
                        player_name = player_n.replace("'", "")
                        val_str = cells[len(cells)-1].getText()
                        val_str2 = val_str.replace(u'\xa0', u'')
                        val = 0 if val_str2=='' else int(val_str)
                            

                        # Add to database
                        game_number = int((i+7)/8) if season==61 else int((i+8)/9)
                        data = str(id_) + ", '" + player_name + "', '" + team_names[team_pos] + "', '" + team_names[other_pos[team_pos]] + "', " + str(season) + ", " + str(game_number) + ", " + str(val)
                        sql = "INSERT INTO Players VALUES (%s);" % data
                        cursor.execute(sql)
                        # Update id
                        id_ += 1

            # Close connection with website
            sock.close()
        j += 1
    # Commit to save changes
    connection.commit()

finally:
    connection.close()







