NUM_GAMES = 1230
FIRST_MATCHES = 200
FIRST_YEAR, LAST_YEAR = 19, 19
NUM_SEASONS = LAST_YEAR - FIRST_YEAR + 1

INDEX_GAME_SUMMARY = 0
INDEX_TEAM_ID = 3
INDEX_LINE_SCORE = 5
INDEX_SEASON = 8
INDEX_POINTS = 22

MATCHES_PARAMETERS = ["home win percentage", "home last 5 wins", "home avg points", "home last 5 points",
                    "away win percentage", "away last 5 wins", "away avg points", "away last 5 points",
                    "winner"]

FILE_MATCHES_DATA = "matches.csv"
FILE_CLASSIFIER = "quadratic_discriminant_analysis.pickle"
