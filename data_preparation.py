import const
from utils import add_trailing_zeros

import pandas as pd
import numpy as np


def remove_seconds(time):
    minutes, _ = time.split(":")
    return minutes


def adjust_per_hour(matches):
    # find all numerical attributes
    att_num = matches.select_dtypes([np.number]).drop(columns=const.IDENTIFIERS).columns

    # convert minutes from string to integer
    matches["minutes"] = pd.to_numeric(matches["minutes"], downcast="integer")

    # adjust all numerical attributes per minute
    matches[att_num] = matches[att_num].div(matches["minutes"], axis="index")

    # adjust all numerical attributes per hour
    matches[att_num] = matches[att_num].mul(60)

    return matches


def retrive_seasons(game_ids):
    # define the target seasons
    seasons_threshold = list(range(const.FIRST_YEAR - 1, const.LAST_YEAR + 1))
    # define the edges of the intervals used to segment the matches
    matches_threshold = [add_trailing_zeros(season + 200, n_zeros=5) for season in seasons_threshold]

    # assign to each match the corresponding season
    seasons = pd.cut(game_ids, bins=matches_threshold, labels=const.SEASONS).astype("int8")

    return seasons


def processes_data(matches):
    # add more identifying attributes
    matches["season"] = retrive_seasons(matches["game id"])
    matches["game num"] = matches.groupby("season").cumcount()

    # adjust attributes per hour
    matches["minutes"] = matches["minutes"].map(remove_seconds)
    matches = adjust_per_hour(matches)

    return matches


def prepare_data():
    matches = pd.read_csv(const.FILE_RAW)

    matches_processed = processes_data(matches)
    matches_processed.to_csv(const.FILE_PROCESSED, index=False)
