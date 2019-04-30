import Team

import pandas as pd
from nba_api.stats.endpoints import boxscoresummaryv2


TEAMS_DATA = []
MATCHES_DATA = pd.DataFrame()


def add_digits(num, digits):
    num_digits = sum(1 for _ in str(num))
    return ''.join('0' for _ in range(digits - num_digits)) + str(num)

def calculate_game_id(year, game_number):
    return "002" + add_digits(year - 1, 2) + add_digits(game_number, 5)

def get_games_id():
    MIN_GAMES_PER_TEAM_BEFORE_COMPUTING = 5
    NUM_GAMES = 1230
    NUM_TEAMS = 30

    min_games = MIN_GAMES_PER_TEAM_BEFORE_COMPUTING * (NUM_TEAMS // 2)
    first_year, last_year = 19, 19
    years = (year for year in range(first_year, last_year + 1))
    
    for year in years:
        for game_number in range(min_games + 1, NUM_GAMES + 1):
            yield calculate_game_id(year, game_number)

def get_game(game_id):
    boxscoresummary = boxscoresummaryv2.BoxScoreSummaryV2(game_id).get_dict()
    boxscoresummary = boxscoresummary.get("resultSets")
    return boxscoresummary

def get_game_summary(game):
    index_game_summary = 0
    game_summary = game[index_game_summary]["headers"]
    return game_summary

def get_line_score(game):
    index_line_score = 5
    line_score = game[index_line_score]["rowSet"]
    return line_score

def get_team_id(game):
    index_team_id = 3
    
    home_line_score, away_line_score = get_line_score(game)
    home_team_id, away_team_id = home_line_score[index_team_id], away_line_score[index_team_id]
    return home_team_id, away_team_id

def get_season(game):
    index_season = 8
    season = get_game_summary(game)[index_season]
    return season

def get_points(game):
    index_points = 22

    home_line_score, away_line_score = get_line_score(game)
    home_points, away_points = home_line_score[index_points], away_line_score[index_points]
    return home_points, away_points

def add_team(id, season):
    TEAMS_DATA.append(Team.Team(id, season))

def get_team(id, new_season=None):
    if new_season is None:
        team = next((team for team in TEAMS_DATA if team.id == id), None)
    else:
        team = next((team for team in TEAMS_DATA if team.id == id), add_team(id, new_season))
    return team

def update_match(home_id, away_id, winner):
    global MATCHES_DATA
    home, away = get_team(home_id), get_team(away_id)
    home_data = [home.get_win_percentage(), home.get_avg_points(), home.plus_minus]
    away_data = [away.get_win_percentage, away.get_avg_points(), away.plus_minus]
    home_and_away = home_data + away_data
    parameters = ["home win percentage", "home avg points", "home plus minus", 
                "away win percentage", "away avg points", "away plus minus",
                "winner"]

    new_match = pd.DataFrame([home_and_away + [winner]], columns=parameters)
    MATCHES_DATA = MATCHES_DATA.append(new_match, ignore_index=True)

def update_team(team_id, season, points, opponents_points):
    team = get_team(team_id, season)
    team.season = season
    team.update(points, opponents_points)

def retrive_data(game):
    season = get_season(game)
    home_team_id, away_team_id = get_team_id(game)
    home_points, away_points = get_points(game)
    winner = 0 if home_points > away_points else 1

    update_team(home_team_id, season, home_points, away_points)
    update_team(away_team_id, season, away_points, home_points)
    update_match(home_team_id, away_team_id, winner)

if __name__ == '__main__':
    for i, game_id in enumerate(get_games_id()):
        game = get_game(game_id)
        retrive_data(game)
