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
FIELDS = ["home", "away"]


""" for data processing """
# ATOMIC ATTRIBUTES
ATT_ATOMIC = ["pts", "fgm", "ftm", "fg3m", "eff", "pir", "win",
              "off rating", "def rating", "eft pct", "ts pct", "salary"]
ATT_MAIN = [f"{field} {att}" for att in ATT_ATOMIC for field in FIELDS]

# DIFFERENCES ATTRIBUTES
ATT_FOR_DIFF = ATT_MAIN
ATT_FOR_DIFF_HOME, ATT_FOR_DIFF_AWAY = ATT_FOR_DIFF[0::2], ATT_FOR_DIFF[1::2]
ATT_DIFF = [f"{att} diff" for att in ATT_FOR_DIFF]
ATT_DIFF_HOME, ATT_DIFF_AWAY = ATT_DIFF[0::2], ATT_DIFF[1::2]


FILE_RAW = "matches_raw.csv"
FILE_PROCESSED  = "matches_processed.csv"
FILE_CLASSIFIER = "logistic_regression.pickle"
