NUM_GAMES = 1230
FIRST_MATCHES = 200
FIRST_YEAR, LAST_YEAR = 5, 19
NUM_SEASONS = LAST_YEAR - FIRST_YEAR + 1
SEASONS = list(range(FIRST_YEAR, LAST_YEAR + 1))

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


WIN_HOME, WIN_AWAY = 0, 1
IDENTIFIERS = ["game id", "home id", "away id", "season", "game num"]

FILE_RAW = "matches_raw.csv"
FILE_PROCESSED  = "matches_processed.csv"
FILE_CLASSIFIER = "logistic_regression.pickle"
