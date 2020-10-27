NUM_GAMES = 1230
FIRST_MATCHES = 200
FIRST_YEAR, LAST_YEAR = 5, 19
NUM_SEASONS = LAST_YEAR - FIRST_YEAR + 1

INDEX_GAME_ID    = 0
INDEX_TEAM_STATS = 1
INDEX_MIN        = 5
INDEXES_ATTRIBUTES = {
    "id"  : 1,
    "name": 2,
    "fgm" : 6,
    "fga" : 7,
    "fg3m": 9,
    "fg3a": 10,
    "ftm" : 12,
    "fta" : 13,
    "oreb": 15,
    "dreb": 16,
    "reb" : 17,
    "ast" : 18,
    "stl" : 19,
    "blk" : 20,
    "to"  : 21,
    "pf"  : 22,
    "pts" : 23
}


MATCHES_PARAMETERS_RAW = ["game id",   "home id",  "home name", "home pts",
                          "home fgm",  "home fga", "home fg3m", "home fg3a",
                          "home ftm",  "home fta", "home oreb", "home dreb",
                          "home reb",  "home ast", "home stl",  "home blk",
                          "home to",   "home pf",  "away id",   "away name",
                          "away pts",  "away fgm", "away fga",  "away fg3m",
                          "away fg3a", "away ftm", "away fta",  "away oreb",
                          "away dreb", "away reb", "away ast",  "away stl",
                          "away blk",  "away to",  "away pf"]


FILE_MATCHES_DATA_RAW = "matches_raw.csv"
FILE_CLASSIFIER = "logistic_regression.pickle"
