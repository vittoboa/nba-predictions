import const
from utils import save_dataframe_in_file, get_games_id

import json
import pandas as pd
from nba_api.stats.endpoints import boxscoretraditionalv2


def get_game(game_id):
    try:
        boxscoretraditional = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id).get_dict()
        boxscoretraditional = boxscoretraditional.get("resultSets")
        return boxscoretraditional
    except json.decoder.JSONDecodeError:
        return None


def get_team_stats(game):
    return game[const.INDEX_TEAM_STATS]["rowSet"]


def get_stat(teams_stats, index):
    home_stats, away_stats = teams_stats
    return home_stats[index], away_stats[index]


def get_match_data_as_dataframe(game):
    teams_stats = get_team_stats(game)

    data = {}

    # retrive the value for the match attributes
    data["game id"], _ = get_stat(teams_stats, const.INDEX_GAME_ID)
    data["minutes"], _ = get_stat(teams_stats, const.INDEX_MIN)
    # retrive the value of each attribute for the home and away team
    for att_name, index in const.INDEXES_ATTRIBUTES.items():
        att_name_home, att_name_away = f"home {att_name}", f"away {att_name}"
        data[att_name_home], data[att_name_away] = get_stat(teams_stats, index)

    data_values, data_names = data.values(), data.keys()

    return pd.DataFrame([data_values], columns=data_names)


def save_matches_timeline(filename):
    print('Retriving previous matches to train classifier...')

    matches_data = pd.DataFrame()

    for season in range(const.FIRST_YEAR, const.LAST_YEAR + 1):
        for game_id in get_games_id(season):
            game = get_game(game_id)
            if game is None:
                break

            match_data = get_match_data_as_dataframe(game)
            matches_data = matches_data.append(match_data, ignore_index=True)

    save_dataframe_in_file(matches_data, filename)
