import Team
import const
from utils import (calculate_shooting,
                   calculate_poss,
                   calculate_oreb,
                   calculate_free_thorows,
                   add_digits,
                   save_dataframe_in_file)

import pandas as pd
from nba_api.stats.endpoints import boxscoretraditionalv2


teams_data = []
matches_data = pd.DataFrame()


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


def add_team(id, season):
    teams_data.append(Team.Team(id, season))


def get_team(id, season):
    return next((team for team in teams_data if team.id == id), add_team(id, season))


def update_match(season, home_id, away_id, winner):
    global matches_data
    home, away = get_team(home_id, season), get_team(away_id, season)
    home_data = [home.get_avg_stat('shooting'), home.get_avg_stat('poss'),
                 home.get_avg_stat('oreb'), home.get_avg_stat('free throws'),
                 home.get_avg_stat('shooting', 'def'), home.get_avg_stat('poss', 'def'),
                 home.get_avg_stat('oreb', 'def'), home.get_avg_stat('free throws', 'def')]
    away_data = [away.get_avg_stat('shooting'), away.get_avg_stat('poss'),
                 away.get_avg_stat('oreb'), away.get_avg_stat('free throws'),
                 away.get_avg_stat('shooting', 'def'), away.get_avg_stat('poss', 'def'),
                 away.get_avg_stat('oreb', 'def'), away.get_avg_stat('free throws', 'def')]

    home_and_away = home_data + away_data

    new_match = pd.DataFrame([home_and_away + [winner]], columns=const.MATCHES_PARAMETERS)
    matches_data = matches_data.append(new_match, ignore_index=True)


def update_team(season, team_id, own_four_factors, opnt_four_factors):
    team = get_team(team_id, season)
    team.season = season
    team.update(own_four_factors["shooting"], opnt_four_factors["shooting"],
                own_four_factors["poss"], opnt_four_factors["poss"],
                own_four_factors["oreb"], opnt_four_factors["oreb"],
                own_four_factors["free throws"], opnt_four_factors["free throws"])


def get_match_data(game):
    teams_stats = get_team_stats(game)
    home = {}
    away = {}

    home["id"], away["id"] = get_stat(teams_stats, const.INDEX_TEAM_ID)
    home["pts"], away["pts"] = get_stat(teams_stats, const.INDEX_POINTS)
    home["fgm"], away["fgm"] = get_stat(teams_stats, const.INDEX_FGM)
    home["fg3m"], away["fg3m"] = get_stat(teams_stats, const.INDEX_FG3M)
    home["fga"], away["fga"] = get_stat(teams_stats, const.INDEX_FGA)
    home["oreb"], away["oreb"] = get_stat(teams_stats, const.INDEX_OREB)
    home["dreb"], away["dreb"] = get_stat(teams_stats, const.INDEX_DREB)
    home["to"], away["to"] = get_stat(teams_stats, const.INDEX_TO)
    home["fta"], away["fta"] = get_stat(teams_stats, const.INDEX_FTA)
    home["ftm"], away["ftm"] = get_stat(teams_stats, const.INDEX_FTM)

    return home, away


def get_winner(home_data, away_data):
    home, away = 0, 1
    return home if home_data["pts"] > away_data["pts"] else away


def get_four_factores(home, away):
    home_four_factors = {}
    away_four_factors = {}

    home_four_factors["shooting"] = calculate_shooting(home["fgm"], home["fg3m"], home["fga"])
    away_four_factors["shooting"] = calculate_shooting(away["fgm"], away["fg3m"], away["fga"])
    home_four_factors["poss"] = calculate_poss(home["fga"], home["oreb"], home["to"], home["fta"])
    away_four_factors["poss"] = calculate_poss(away["fga"], away["oreb"], away["to"], away["fta"])
    home_four_factors["oreb"] = calculate_oreb(home["oreb"], away["dreb"])
    away_four_factors["oreb"] = calculate_oreb(away["oreb"], home["dreb"])
    home_four_factors["free throws"] = calculate_free_thorows(home["ftm"], home["fga"])
    away_four_factors["free throws"] = calculate_free_thorows(away["ftm"], away["fga"])

    return home_four_factors, away_four_factors


def update_saved_data(season, home_data, away_data):
    home_id, away_id = home_data["id"], away_data["id"]
    home_four_factors, away_four_factors = get_four_factores(home_data, away_data)
    winner = get_winner(home_data, away_data)

    update_match(season, home_id, away_id, winner)

    update_team(season, home_id, home_four_factors, away_four_factors)
    update_team(season, away_id, away_four_factors, home_four_factors)


def save_matches_timeline(filename):
    print('Retriving previous matches to train classifier...')

    for season in range(const.FIRST_YEAR, const.LAST_YEAR + 1):
        for game_id in get_games_id(season):
            game = get_game(game_id)
            home_data, away_data = get_match_data(game)
            update_saved_data(season, home_data, away_data)

    save_dataframe_in_file(matches_data, filename)
