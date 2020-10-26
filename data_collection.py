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

    home, away = {}, {}

    game_id, _ = get_stat(teams_stats, const.INDEX_GAME_ID)
    minutes, _ = get_stat(teams_stats, const.INDEX_MIN)
    home["id"],   away["id"]   = get_stat(teams_stats, const.INDEX_TEAM_ID)
    home["name"], away["name"] = get_stat(teams_stats, const.INDEX_TEAM_NAME)
    home["pts"],  away["pts"]  = get_stat(teams_stats, const.INDEX_PTS)
    home["fgm"],  away["fgm"]  = get_stat(teams_stats, const.INDEX_FGM)
    home["fga"],  away["fga"]  = get_stat(teams_stats, const.INDEX_FGA)
    home["fg3m"], away["fg3m"] = get_stat(teams_stats, const.INDEX_FG3M)
    home["fg3a"], away["fg3a"] = get_stat(teams_stats, const.INDEX_FG3A)
    home["ftm"],  away["ftm"]  = get_stat(teams_stats, const.INDEX_FTM)
    home["fta"],  away["fta"]  = get_stat(teams_stats, const.INDEX_FTA)
    home["oreb"], away["oreb"] = get_stat(teams_stats, const.INDEX_OREB)
    home["dreb"], away["dreb"] = get_stat(teams_stats, const.INDEX_DREB)
    home["reb"],  away["reb"]  = get_stat(teams_stats, const.INDEX_REB)
    home["ast"],  away["ast"]  = get_stat(teams_stats, const.INDEX_AST)
    home["stl"],  away["stl"]  = get_stat(teams_stats, const.INDEX_STL)
    home["blk"],  away["blk"]  = get_stat(teams_stats, const.INDEX_BLK)
    home["to"],   away["to"]   = get_stat(teams_stats, const.INDEX_TO)
    home["pf"],   away["pf"]   = get_stat(teams_stats, const.INDEX_PF)

    match_data = [game_id, minutes, *home.values(), *away.values()]

    return pd.DataFrame([match_data], columns=const.MATCHES_PARAMETERS_RAW)


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
