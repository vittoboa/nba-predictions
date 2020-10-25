NUM_GAMES = 1230
FIRST_MATCHES = 200
FIRST_YEAR, LAST_YEAR = 5, 19
NUM_SEASONS = LAST_YEAR - FIRST_YEAR + 1

INDEX_TEAM_STATS = 1
INDEX_GAME_ID    = 0
INDEX_TEAM_ID    = 1
INDEX_TEAM_NAME  = 2
INDEX_FGM        = 6
INDEX_FGA        = 7
INDEX_FG3M       = 9
INDEX_FG3A       = 10
INDEX_FTM        = 12
INDEX_FTA        = 13
INDEX_OREB       = 15
INDEX_DREB       = 16
INDEX_REB        = 17
INDEX_AST        = 18
INDEX_STL        = 19
INDEX_BLK        = 20
INDEX_TO         = 21
INDEX_PF         = 22
INDEX_PTS        = 23

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
