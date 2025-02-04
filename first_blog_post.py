import json
import os
import requests
import pandas as pd
from player_dict import player_id_dict_by_team


def get_player_shot_log(player_id):
    #NBA Stats API using selected player ID
    url = 'http://stats.nba.com/stats/playerdashptshotlog?'+ \
    'DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&' + \
    'Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&' + \
    'PlayerID='+player_id+'&Season=2014-15&SeasonSegment=&' + \
    'SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision='

    #Create Dict based on JSON response
    response = requests.get(url)
    shots = response.json()['resultSets'][0]['rowSet']
    data = json.loads(response.text)

    #Create df from data and find averages
    headers = data['resultSets'][0]['headers']
    shot_data = data['resultSets'][0]['rowSet']
    df = pd.DataFrame(shot_data,columns=headers)
    return(df)


def get_all_shot_logs():
    all_shot_logs = []
    for team_dict in player_id_dict_by_team.values():
        for player_name in team_dict:
            player_id   = team_dict[player_name]
            shot_log    = get_player_shot_log(player_id)
            shot_log['player_name']   = player_name
            shot_log['player_id']     = player_id
            all_shot_logs.append(shot_log)
    return(all_shot_logs)


if __name__ == "__main__":
    if "shot_logs.csv" in os.listdir('data'): #if data stored from previous run
        all_shot_logs = pd.read_csv('data/shot_logs.csv')
    else:
        all_shot_logs=pd.concat(get_all_shot_logs())
        all_shot_logs.to_csv('shot_logs.csv')

player_in_game_grouping = all_shot_logs.groupby(['GAME_ID', 'player_id'])
fgm_cum     = player_in_game_grouping.FGM.cumsum()
fga_cum     = player_in_game_grouping.cumcount()

