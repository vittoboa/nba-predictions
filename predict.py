def ask_team_name(court):
    return input(court + ' team name: ')

def ask_win_percentage(court):
    return float(input(court + ' team win percentage: '))

def ask_avg_points(court):
    return float(input(court + ' team average points per game: '))

def ask_last_5_wins(court):
    return float(input(court + ' team wins in the last 5 matches: '))

def ask_last_5_points(court):
    return float(input(court + ' team points in the last 5 matches: '))

def get_team_data(court):
    team_data = []
    team_data.append(ask_win_percentage(court))
    team_data.append(ask_last_5_wins(court))
    team_data.append(ask_avg_points(court))
    team_data.append(ask_last_5_points(court))

    return team_data

def main():
    """ ask the user about the teams data """
    print('Enter the following informations about the match that needs to be predicted.')
    team_home_name, team_home_data = ask_team_name('Home'), get_team_data('Home')
    team_away_name, team_away_data = ask_team_name('Away'), get_team_data('Away')
    teams_data = team_home_data + team_away_data


if __name__ == '__main__':
    main()
