import Team

import pandas as pd
from nba_api.stats.endpoints import boxscoresummaryv2


TEAMS_DATA = []
MATCHES_DATA = pd.DataFrame()


def save_to_file(file_name):
    MATCHES_DATA.to_csv(file_name, index=False)

def add_digits(num, digits):
    num_digits = sum(1 for _ in str(num))
    return ''.join('0' for _ in range(digits - num_digits)) + str(num)

def calculate_game_id(year, game_number):
    return "002" + add_digits(year - 1, 2) + add_digits(game_number, 5)

def get_games_id():
    NUM_GAMES = 1230
    first_year, last_year = 19, 19
    years = (year for year in range(first_year, last_year + 1))
    
    for year in years:
        for game_number in range(1, NUM_GAMES + 1):
            yield calculate_game_id(year, game_number)

def get_game(game_id):
    boxscoresummary = boxscoresummaryv2.BoxScoreSummaryV2(game_id).get_dict()
    boxscoresummary = boxscoresummary.get("resultSets")
    return boxscoresummary

def get_game_summary(game):
    index_game_summary = 0
    game_summary = game[index_game_summary]["rowSet"][0]
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

def get_team(id, season):
    return next((team for team in TEAMS_DATA if team.id == id), add_team(id, season))

def update_match(season, home_id, away_id, winner):
    global MATCHES_DATA
    home, away = get_team(home_id, season), get_team(away_id, season)
    home_data = [home.get_win_percentage(), home.get_last_5_wins(), home.get_avg_points(), home.get_last_5_points()]
    away_data = [away.get_win_percentage(), away.get_last_5_wins(), away.get_avg_points(), away.get_last_5_points()]
    home_and_away = home_data + away_data
    parameters = ["home win percentage", "home last 5 wins", "home avg points", "home last 5 points",
                "away win percentage", "away last 5 wins", "away avg points", "away last 5 points",
                "winner"]

    new_match = pd.DataFrame([home_and_away + [winner]], columns=parameters)
    MATCHES_DATA = MATCHES_DATA.append(new_match, ignore_index=True)

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


if __name__ == '__main__':
    for game_id in get_games_id():
        game = get_game(game_id)
        retrive_data(game)

    save_to_file("matches.csv")
