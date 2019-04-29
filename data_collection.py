from nba_api.stats.endpoints import boxscoresummaryv2, teamdashboardbylastngames


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
    game_summary = boxscoresummaryv2.BoxScoreSummaryV2(game_id).get_dict()
    game_summary = game_summary.get("resultSets")
    return game_summary

def data_collection():
    for game_id in get_games_id():
        game = get_game(game_id)
        print(game_id)


data_collection()