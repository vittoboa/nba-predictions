import const
from utils import add_digits, save_dataframe_in_file

import pandas as pd
from nba_api.stats.endpoints import boxscoretraditionalv2


def calculate_game_id(year, game_number):
    return "002" + add_digits(year - 1, 2) + add_digits(game_number, 5)


def get_games_id(year):
    for game_number in range(1, const.NUM_GAMES + 1):
        yield calculate_game_id(year, game_number)


def get_game(game_id):
    boxscoretraditional = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id).get_dict()
    boxscoretraditional = boxscoretraditional.get("resultSets")
    return boxscoretraditional


def get_team_stats(game):
    return game[const.INDEX_TEAM_STATS]["rowSet"]


def get_stat(teams_stats, index):
    home_stats, away_stats = teams_stats
    return home_stats[index], away_stats[index]


def get_match_data_as_dataframe(game_id):
    game = get_game(game_id)
    teams_stats = get_team_stats(game)

    home_id,   away_id   = get_stat(teams_stats, const.INDEX_TEAM_ID)
    home_name, away_name = get_stat(teams_stats, const.INDEX_TEAM_NAME)
    home_pts,  away_pts  = get_stat(teams_stats, const.INDEX_PTS)
    home_fgm,  away_fgm  = get_stat(teams_stats, const.INDEX_FGM)
    home_fga,  away_fga  = get_stat(teams_stats, const.INDEX_FGA)
    home_fg3m, away_fg3m = get_stat(teams_stats, const.INDEX_FG3M)
    home_fg3a, away_fg3a = get_stat(teams_stats, const.INDEX_FG3A)
    home_ftm,  away_ftm  = get_stat(teams_stats, const.INDEX_FTM)
    home_fta,  away_fta  = get_stat(teams_stats, const.INDEX_FTA)
    home_oreb, away_oreb = get_stat(teams_stats, const.INDEX_OREB)
    home_dreb, away_dreb = get_stat(teams_stats, const.INDEX_DREB)
    home_reb,  away_reb  = get_stat(teams_stats, const.INDEX_REB)
    home_ast,  away_ast  = get_stat(teams_stats, const.INDEX_AST)
    home_stl,  away_stl  = get_stat(teams_stats, const.INDEX_STL)
    home_blk,  away_blk  = get_stat(teams_stats, const.INDEX_BLK)
    home_to,   away_to   = get_stat(teams_stats, const.INDEX_TO)
    home_pf,   away_pf   = get_stat(teams_stats, const.INDEX_PF)

    home_data = [home_id, home_name, home_pts, home_fgm, home_fga, home_fg3m,
                 home_fg3a, home_ftm, home_fta, home_oreb, home_dreb, home_reb,
                 home_ast, home_stl, home_blk, home_to, home_pf]

    away_data = [away_id, away_name, away_pts, away_fgm, away_fga, away_fg3m,
                 away_fg3a, away_ftm, away_fta, away_oreb, away_dreb, away_reb,
                 away_ast, away_stl, away_blk, away_to, away_pf]

    return pd.DataFrame([[game_id] + home_data + away_data], columns=const.MATCHES_PARAMETERS_RAW)


def save_matches_timeline(filename):
    print('Retriving previous matches to train classifier...')

    matches_data = pd.DataFrame()

    for season in range(const.FIRST_YEAR, const.LAST_YEAR + 1):
        for game_id in get_games_id(season):
            match_data = get_match_data_as_dataframe(game_id)
            matches_data = matches_data.append(match_data, ignore_index=True)

    save_dataframe_in_file(matches_data, filename)
