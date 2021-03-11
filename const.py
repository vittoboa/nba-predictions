NUM_GAMES = 1230
FIRST_MATCHES = 200
FIRST_YEAR, LAST_YEAR = 5, 19
NUM_SEASONS = LAST_YEAR - FIRST_YEAR + 1
SEASONS = list(range(FIRST_YEAR, LAST_YEAR + 1))
MATCH_MINUTES_THRESHOLD = 237
DEFAULT_REST_DAYS = 4

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
TARGET = "winner"


""" for data processing """
# ATOMIC ATTRIBUTES
ATT_ATOMIC = ["pts", "fgm", "ftm", "fg3m", "eff", "pir", "win",
              "off rating", "def rating", "eft pct", "ts pct", "salary"]
ATT_MAIN = [f"{field} {att}" for att in ATT_ATOMIC for field in FIELDS]

# PERCENTAGES ATTRIBUTES
#                           {value_attribute: tot_attribute}
ATT_FOR_PERCENTAGE_ATOMIC = {"fgm": "fga", "ftm": "fta", "fg3m": "fg3a"}
ATT_FOR_PERCENTAGE = {f"{field} {att_val}": f"{field} {att_tot}"
                      for att_val, att_tot in ATT_FOR_PERCENTAGE_ATOMIC.items()
                      for field in FIELDS}
ATT_PCT = [f"{field} {att} pct"
           for att in ATT_FOR_PERCENTAGE_ATOMIC for field in FIELDS]

# DIFFERENCES ATTRIBUTES
ATT_FOR_DIFF = [*ATT_MAIN, *ATT_PCT]
ATT_FOR_DIFF_HOME, ATT_FOR_DIFF_AWAY = ATT_FOR_DIFF[0::2], ATT_FOR_DIFF[1::2]
ATT_DIFF = [f"{att} diff" for att in ATT_FOR_DIFF]
ATT_DIFF_HOME, ATT_DIFF_AWAY = ATT_DIFF[0::2], ATT_DIFF[1::2]

# PROCESSED ATTRIBUTES
ATT_PROCESSED = [*ATT_FOR_DIFF, *ATT_DIFF]
ATT_PRC_HOME, ATT_PRC_AWAY = ATT_PROCESSED[0::2], ATT_PROCESSED[1::2]


""" for data aggregation """
# AVERAGES ATTRIBUTES
ATT_AVG = [f"{name} avg" for name in ATT_PROCESSED]
ATT_AVG_HOME, ATT_AVG_AWAY = ATT_AVG[0::2], ATT_AVG[1::2]

# MEDIANS ATTRIBUTES
ATT_MEDIAN = [f"{name} diff from median" for name in ATT_PROCESSED]
ATT_MEDIAN_HOME, ATT_MEDIAN_AWAY = ATT_MEDIAN[0::2], ATT_MEDIAN[1::2]

# AGGREGATED ATTRIBUTES
ATT_AGG_CURR_SEASON = [*ATT_AVG, *ATT_MEDIAN]
ATT_AGG_PAST_SEASON = [f"{col_name} past season" for col_name in ATT_AGG_CURR_SEASON]
ATT_SEASON_HOME, ATT_SEASON_AWAY = ATT_AGG_PAST_SEASON[0::2], ATT_AGG_PAST_SEASON[1::2]
ATT_AGGREGATED = [*ATT_AGG_CURR_SEASON, *ATT_AGG_PAST_SEASON]
ATT_AGG_HOME, ATT_AGG_AWAY = ATT_AGGREGATED[0::2], ATT_AGGREGATED[1::2]

FILE_RAW = "matches_raw.csv"
FILE_PROCESSED  = "matches_processed.csv"
FILE_CLASSIFIER = "logistic_regression.pickle"
