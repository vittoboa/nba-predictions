import const
import utils

import pandas as pd
import numpy as np


def add_efficiency(matches):
    # retrive the required data to calculate team's efficiency
    target_atts = ["pts", "reb", "ast", "stl", "blk", "fga", "fgm", "fta", "ftm", "to"]
    home_values, away_values = {}, {}
    for att in target_atts:
        home_value, away_value = matches[[f"home {att}", f"away {att}"]].values.T
        home_values[att] = home_value
        away_values[att] = away_value

    # calculate missed shots
    home_missed_fg = home_values["fga"] - home_values["fgm"]
    away_missed_fg = away_values["fga"] - away_values["fgm"]
    home_missed_ft = home_values["fta"] - home_values["ftm"]
    away_missed_ft = away_values["fta"] - away_values["ftm"]

    # calculate efficiency
    home_eff = utils.calculate_efficiency(
        home_values["pts"], home_values["reb"], home_values["ast"], home_values["stl"],
        home_values["blk"], home_missed_fg, home_missed_ft, home_values["to"])
    away_eff = utils.calculate_efficiency(
        away_values["pts"], away_values["reb"], away_values["ast"], away_values["stl"],
        away_values["blk"], away_missed_fg, away_missed_ft, away_values["to"])

    matches["home eff"] = home_eff
    matches["away eff"] = away_eff

    return matches


def add_pir(matches):
    # retrive the required data to calculate team's Performance Index Rating
    target_atts = ["pts", "reb", "ast", "stl", "blk", "fga", "fgm", "fta", "ftm", "to", "pf"]
    home_values, away_values = {}, {}
    for att in target_atts:
        home_value, away_value = matches[[f"home {att}", f"away {att}"]].values.T
        home_values[att] = home_value
        away_values[att] = away_value

    # calculate missed shots
    home_missed_fg = home_values["fga"] - home_values["fgm"]
    away_missed_fg = away_values["fga"] - away_values["fgm"]
    home_missed_ft = home_values["fta"] - home_values["ftm"]
    away_missed_ft = away_values["fta"] - away_values["ftm"]

    # calculate pir
    home_pir = utils.calculate_pir(
        home_values["pts"], home_values["reb"], home_values["ast"], home_values["stl"],
        home_values["blk"], away_values["pf"], home_missed_fg, home_missed_ft,
        home_values["to"], away_values["blk"], home_values["pf"])
    away_pir = utils.calculate_pir(
        away_values["pts"], away_values["reb"], away_values["ast"], away_values["stl"],
        away_values["blk"], home_values["pf"], away_missed_fg, away_missed_ft,
        away_values["to"], home_values["blk"], away_values["pf"])

    matches["home pir"] = home_pir
    matches["away pir"] = away_pir

    return matches


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


def add_winners(matches):
    # determine in which matches the home team won
    is_winner_home = matches["home pts"].values > matches["away pts"].values

    # set 1 if the home team has won, otherwise 0
    matches["home win"] = is_winner_home.astype("int8")
    # set 1 if the home team has lost, otherwise 0
    matches["away win"] = (~is_winner_home).astype("int8")
    # set the win_home value where the home team has won, otherwise the win_away value
    matches["winner"] = np.where(is_winner_home, const.WIN_HOME, const.WIN_AWAY)

    return matches


def add_eft_pct(matches):
    # retrive the required data to calculate team's EFT percentage
    home_fga,  away_fga  = matches[["home fga", "away fga"]].values.T
    home_fgm,  away_fgm  = matches[["home fgm", "away fgm"]].values.T
    home_fg3m, away_fg3m = matches[["home fg3m", "away fg3m"]].values.T

    matches["home eft pct"] = utils.calculate_eft_pct(home_fgm, home_fg3m, home_fga)
    matches["away eft pct"] = utils.calculate_eft_pct(away_fgm, away_fg3m, away_fga)

    return matches


def add_ts_pct(matches):
    # retrive the required data to calculate team's true shooting percentage
    home_pts, away_pts = matches[["home pts", "away pts"]].values.T
    home_fga, away_fga = matches[["home fga", "away fga"]].values.T
    home_fta, away_fta = matches[["home fta", "away fta"]].values.T

    matches["home ts pct"] = utils.calculate_ts_pct(home_pts, home_fga, home_fta)
    matches["away ts pct"] = utils.calculate_ts_pct(away_pts, away_fga, away_fta)

    return matches


def retrive_seasons(game_ids):
    # define the target seasons
    seasons_threshold = list(range(const.FIRST_YEAR - 1, const.LAST_YEAR + 1))
    # define the edges of the intervals used to segment the matches
    matches_threshold = [utils.add_trailing_zeros(season + 200, n_zeros=5) for season in seasons_threshold]

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

    # add more attributes using existing data
    matches = add_winners(matches)
    matches = add_efficiency(matches)
    matches = add_pir(matches)
    matches = add_eft_pct(matches)
    matches = add_ts_pct(matches)

    return matches


def prepare_data():
    matches = pd.read_csv(const.FILE_RAW)

    matches_processed = processes_data(matches)
    matches_processed.to_csv(const.FILE_PROCESSED, index=False)
