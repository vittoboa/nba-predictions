import Team
import const

import pandas as pd
from nba_api.stats.endpoints import boxscoresummaryv2


teams_data = []
matches_data = pd.DataFrame()


def save_to_file(file_name):
    matches_data.to_csv(file_name, index=False)

def add_digits(num, digits):
    num_digits = sum(1 for _ in str(num))
    return ''.join('0' for _ in range(digits - num_digits)) + str(num)

def calculate_game_id(year, game_number):
    return "002" + add_digits(year - 1, 2) + add_digits(game_number, 5)

def get_games_id():
    years = (year for year in range(const.FIRST_YEAR, const.LAST_YEAR + 1))
    
    for year in years:
        for game_number in range(1, const.NUM_GAMES + 1):
            yield calculate_game_id(year, game_number)

def get_game(game_id):
    boxscoresummary = boxscoresummaryv2.BoxScoreSummaryV2(game_id).get_dict()
    boxscoresummary = boxscoresummary.get("resultSets")
    return boxscoresummary

def get_game_summary(game):
    game_summary = game[const.INDEX_GAME_SUMMARY]["rowSet"][0]
    return game_summary

def get_line_score(game):
    line_score = game[const.INDEX_LINE_SCORE]["rowSet"]
    return line_score

def get_team_id(game):
    home_line_score, away_line_score = get_line_score(game)
    home_team_id = home_line_score[const.INDEX_TEAM_ID]
    away_team_id = away_line_score[const.INDEX_TEAM_ID]
    return home_team_id, away_team_id

def get_season(game):
    season = get_game_summary(game)[const.INDEX_SEASON]
    return season

def get_points(game):
    home_line_score, away_line_score = get_line_score(game)
    home_points = home_line_score[const.INDEX_POINTS]
    away_points = away_line_score[const.INDEX_POINTS]
    return home_points, away_points

def add_team(id, season):
    teams_data.append(Team.Team(id, season))

def get_team(id, season):
    return next((team for team in teams_data if team.id == id), add_team(id, season))

def update_match(season, home_id, away_id, winner):
    global matches_data
    home, away = get_team(home_id, season), get_team(away_id, season)
    home_data = [home.get_win_percentage(), home.get_last_5_wins(), home.get_avg_points(), home.get_last_5_points()]
    away_data = [away.get_win_percentage(), away.get_last_5_wins(), away.get_avg_points(), away.get_last_5_points()]
    home_and_away = home_data + away_data

    new_match = pd.DataFrame([home_and_away + [winner]], columns=const.MATCHES_PARAMETERS)
    matches_data = matches_data.append(new_match, ignore_index=True)

def update_team(season, team_id, points, opponents_points):
    team = get_team(team_id, season)
    team.season = season
    team.update(points, opponents_points)

def retrive_data(game):
    season = get_season(game)
    home_team_id, away_team_id = get_team_id(game)
    home_points, away_points = get_points(game)
    winner = 0 if home_points > away_points else 1

    update_match(season, home_team_id, away_team_id, winner)
    update_team(season, home_team_id, home_points, away_points)
    update_team(season, away_team_id, away_points, home_points)

def save_matches_timeline(filename):
    print('Retriving previous matches to train classifier...')
    for game_id in get_games_id():
        game = get_game(game_id)
        retrive_data(game)

    save_to_file(filename)
