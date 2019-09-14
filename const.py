NUM_GAMES = 1230
FIRST_MATCHES = 200
FIRST_YEAR, LAST_YEAR = 19, 19
NUM_SEASONS = LAST_YEAR - FIRST_YEAR + 1

INDEX_TEAM_STATS = 1
INDEX_TEAM_ID = 1
INDEX_FGM = 6
INDEX_FGA = 7
INDEX_FG3M = 9
INDEX_FTM = 12
INDEX_FTA = 13
INDEX_OREB = 15
INDEX_DREB = 16
INDEX_TO = 21
INDEX_POINTS = 23

FOUR_FACTORS = ("shooting", "poss", "oreb", "free throws")
TARGET = "winner"
MATCHES_PARAMETERS = ["home avg win", "home avg off points", "home avg off shooting",
                      "home avg off poss", "home avg off oreb", "home avg off ft", "home avg def points",
                      "home avg def shooting", "home avg def poss", "home avg def oreb",
                      "home avg def ft", "away avg win", "away avg off points", "away avg off shooting",
                      "away avg off poss", "away avg off oreb", "away avg off ft",
                      "away avg def points", "away avg def shooting", "away avg def poss",
                      "away avg def oreb", "away avg def ft", TARGET]

FILE_MATCHES_DATA = "matches.csv"
FILE_CLASSIFIER = "logistic_regression.pickle"
