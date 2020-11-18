import const

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


def processes_data(matches):
    matches["minutes"] = matches["minutes"].map(remove_seconds)
    matches = adjust_per_hour(matches)

    return matches


def prepare_data():
    matches = pd.read_csv(const.FILE_RAW)

    matches_processed = processes_data(matches)
    matches_processed.to_csv(const.FILE_PROCESSED, index=False)
