import const
import utils

import pandas as pd
import numpy as np
from sklearn.preprocessing import QuantileTransformer


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


def add_percentages(matches):
    vals = matches[const.ATT_FOR_PERCENTAGE].values
    tot  = matches[const.ATT_FOR_PERCENTAGE.values()].values

    matches[const.ATT_PCT] = vals / tot * 100

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


def add_differences_home_away(matches):
    home_values = matches[const.ATT_FOR_DIFF_HOME].values
    away_values = matches[const.ATT_FOR_DIFF_AWAY].values

    # calculate the difference between the values of the team and the opponent
    matches[const.ATT_DIFF_HOME] = home_values - away_values
    matches[const.ATT_DIFF_AWAY] = away_values - home_values

    return matches


def add_ratings(matches):
    # retrive the required data to calculate team's ratings
    home_orb, away_orb = matches[["home oreb", "away oreb"]].values.T
    home_pts, away_pts = matches[["home pts", "away pts"]].values.T
    home_fga, away_fga = matches[["home fga", "away fga"]].values.T
    home_fta, away_fta = matches[["home fta", "away fta"]].values.T
    home_to,  away_to  = matches[["home to", "away to"]].values.T

    # calculate remaining required data to calculate team's ratings
    home_possessions = utils.calculate_possesions(home_fga, home_orb, home_to, home_fta)
    away_possessions = utils.calculate_possesions(away_fga, away_orb, away_to, away_fta)

    home_off_rating = utils.calculate_rating(home_pts, home_possessions)
    home_def_rating = utils.calculate_rating(away_pts, home_possessions)
    away_off_rating = utils.calculate_rating(away_pts, away_possessions)
    away_def_rating = utils.calculate_rating(home_pts, away_possessions)

    matches["home off rating"] = home_off_rating
    matches["home def rating"] = home_def_rating
    matches["away off rating"] = away_off_rating
    matches["away def rating"] = away_def_rating

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


def uniform_by_season(matches):
    # select non-identifying numerical attributes
    target_atts = matches.select_dtypes([np.number]).drop(columns=const.IDENTIFIERS).columns

    # transform the target features to follow a uniform distribution
    for season, season_matches in matches.groupby("season"):
        # define conditions on matches
        n_matches = len(season_matches.index)
        target_matches = season_matches[target_atts]
        target_season = matches["season"].values == season

        uniformed_matches = QuantileTransformer(n_quantiles=n_matches).fit_transform(target_matches)
        matches.loc[target_season, target_atts] = uniformed_matches

    return matches


def retrive_matches(matches, team_id, season, last_match=None, columns=None):
    is_current_season = matches["season"].values == season

    # if no last_match is given, consider all matches of the season
    if last_match is None:
        last_match = matches.loc[is_current_season, "game num"].iloc[-1] + 1

    # if no columns are specified, consider all columns
    if columns is None:
        columns = matches.columns

    # define match conditions
    is_past_game    = matches["game num"].values < last_match
    is_target_match = is_current_season & is_past_game
    # define team conditions
    is_playing_home = matches["home id"].values == team_id
    is_playing_away = matches["away id"].values == team_id

    cols_home = [col for col in columns if "away" not in col]
    cols_away = [col for col in columns if "home" not in col]
    matches_home = matches.loc[is_target_match & is_playing_home, cols_home]
    matches_away = matches.loc[is_target_match & is_playing_away, cols_away]

    team_matches = pd.concat([matches_home, matches_away])
    # sort matches in chronological order
    team_matches = team_matches.sort_index()

    return team_matches


def add_rest_days(matches):
    teams_ids = np.unique(matches[["home id", "away id"]])

    for season in const.SEASONS:
        for team_id in teams_ids:
            season_matches = retrive_matches(matches, team_id, season)

            if season_matches.empty:
                continue

            # the first match doesn't have any previous match
            indexes_matches = season_matches.index[1:]
            target_matches  = season_matches.loc[indexes_matches, "date"]
            # the last match can't be a previous match
            indexes_matches_previous = season_matches.index[:-1]
            target_matches_previous  = season_matches.loc[indexes_matches_previous, "date"]

            days_diff = target_matches.sub(target_matches_previous.values)
            days_rest = days_diff.dt.days - 1
            # set arbitrary number of rest days for the first match of the season
            days_rest[season_matches.index[0]] = const.DEFAULT_REST_DAYS

            # define match conditons
            is_playing_home = season_matches["home id"].values == team_id
            is_playing_away = season_matches["away id"].values == team_id
            indexes_playing_home = season_matches[is_playing_home].index
            indexes_playing_away = season_matches[is_playing_away].index

            days_rest_home = days_rest[indexes_playing_home].values
            days_rest_away = days_rest[indexes_playing_away].values
            matches.loc[indexes_playing_home, "home num rest days"] = days_rest_home
            matches.loc[indexes_playing_away, "away num rest days"] = days_rest_away

    # reduce large number of rest days to the default value
    has_many_rest_days = matches[["home num rest days", "away num rest days"]].values > const.DEFAULT_REST_DAYS
    has_many_rest_days_home, has_many_rest_days_away = has_many_rest_days.T
    matches.loc[has_many_rest_days_home, "home num rest days"] = const.DEFAULT_REST_DAYS
    matches.loc[has_many_rest_days_away, "away num rest days"] = const.DEFAULT_REST_DAYS

    return matches


def processes_data(matches):
    # add more identifying attributes
    matches["season"] = retrive_seasons(matches["game id"])
    matches["game num"] = matches.groupby("season").cumcount()

    # adjust attributes per hour
    matches["minutes"] = matches["minutes"].map(remove_seconds)
    matches = adjust_per_hour(matches)
    mask_valid_matches = matches["minutes"].values > const.MATCH_MINUTES_THRESHOLD
    matches = matches[mask_valid_matches]
    matches = matches.drop(columns="minutes")

    # add more attributes using existing data
    matches = add_winners(matches)
    matches = add_efficiency(matches)
    matches = add_pir(matches)
    matches = add_ratings(matches)
    matches = add_eft_pct(matches)
    matches = add_ts_pct(matches)
    matches = add_percentages(matches)
    matches = add_rest_days(matches)

    matches = add_differences_home_away(matches)

    matches = matches.dropna()
    matches = uniform_by_season(matches)

    return matches[[const.TARGET, *const.IDENTIFIERS, *const.ATT_PROCESSED]]


def initialize_columns(matches):
    # add all new columns
    matches = matches.reindex(columns=[*const.ATT_AGGREGATED, *matches.columns])

    # determine the datatypes for all columns
    col_floats = [col for col in matches.columns if matches[col].dtype == "float64"]
    floats   = {col: "float32" for col in col_floats}
    integers = {"winner":  "int8", "home win": "int8", "away win": "int8",
                "game num": "int16",
                "game id": "int32", "home id": "int32",  "away id": "int32"}

    columns_types = {**floats, **integers}
    matches = matches.astype(columns_types)

    return matches


def aggregate_data(matches):
    matches = initialize_columns(matches)

    return matches


def prepare_data():
    matches = pd.read_csv(const.FILE_RAW, parse_dates=["date"])

    matches_processed = processes_data(matches)
    matches_processed.to_csv(const.FILE_PROCESSED, index=False)

    matches_aggregated = aggregate_data(matches_processed)
    matches_aggregated.to_csv(const.FILE_AGGREGATED, index=False)
