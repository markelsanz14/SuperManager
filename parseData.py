import numpy as np

def parseData(input_data, names, teams):
    x, y = [], []
    depth_names = len(names)
    depth_teams = len(teams)
    depth_seasons = 6
    depth_games = 34
    for elem in input_data:
        player = names[elem[1]]
        player_one_hot = np.zeros(depth_names)
        player_one_hot[player] = 1
        team = teams[elem[2]]
        team_one_hot = np.zeros(depth_teams)
        team_one_hot[team] = 1
        rival = teams[elem[3]]
        rival_one_hot = np.zeros(depth_teams)
        rival_one_hot[rival] = 1
        season = elem[4] - 57
        season_one_hot = np.zeros(depth_seasons)
        season_one_hot[season] = 1
        game = elem[5] - 1
        game_one_hot = np.zeros(depth_games)
        game_one_hot[game] = 1
        val = elem[6]
        part1 = np.append(player_one_hot, team_one_hot)
        part2 = np.append(part1, rival_one_hot)
        part3 = np.append(part2, season_one_hot)
        part4 = np.append(part3, game_one_hot)
        x.append(part4)
        y.append([val])
    return x, y
