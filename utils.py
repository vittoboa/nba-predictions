import const
from typing import Tuple, Dict

import pandas as pd


def calculate_shooting(fgm: float, fg3m: float, fga: float) -> float:
    """ effective field goal """
    return (fgm + fg3m/2) / fga


def calculate_poss(fga: float, oreb: float, to: float, fta: float) -> float:
    """ offensive possession """
    return fga - oreb + to + (0.4 * fta)


def calculate_oreb(oreb: float, opponent_dreb: float) -> float:
    """ offensive rebounding """
    return oreb / (oreb + opponent_dreb)


def calculate_free_thorows(ftm: float, fga: float) -> float:
    """ getting to the foul line """
    return ftm / fga


def calculate_ts_pct(pts: float, fga: float, fta: float) -> float:
    """ Team's true shooting percentage.
        Measures the players efficiency at shooting the ball """

    return pts / (2 * (fga + (0.44 * fta)))


def calculate_eft_pct(fgm: float, fg3m: float, fga: float) -> float:
    """ Team's effective technical shooting percentage.
        Adjusts field goal percentage
        to account for the fact that three-point field goals count for three points
        while field goals only count for two points. """

    return (fgm + (0.5 * fg3m)) / fga


def calculate_possesions(fga: float, orb: float, to: float, fta: float) -> float:
    """ Estimate team's possessions """

    return 0.96 * (fga - orb + to + (0.44 * fta))


def calculate_rating(pts: float, possessions: float) -> float:
    """ Calculate defensive and offensive rating.
        Measure offensive or defensive performance.
        For offensive rating use team's points, and
        for defensive rating use opponent's points. """

    return (pts * 100) / possessions


def calculate_efficiency(pts: float, reb: float, ast: float, stl: float, blk: float,
                         missed_fg: float, missed_ft: float, to: float) -> float:
    """ Calculate team's efficiency.
        Accounts for both offensive and defensive contributions """

    return pts + reb + ast + stl + blk - missed_fg - missed_ft - to


def calculate_pir(pts: float, reb: float, ast: float, stl: float, blk: float, pf_opt: float,
                  fg_missed: float, ft_missed: float, to: float, blk_opt: float, pf: float) -> float:
    """ Calculate team's Performance Index Rating. """

    return (pts + reb + ast + stl + blk + pf_opt) - (fg_missed + ft_missed + to + blk_opt + pf)


def get_four_factors(four_factors: Dict[str, float], opnt_dreb: float) -> Dict[str, float]:
    ff = four_factors

    shooting = calculate_shooting(ff["fgm"], ff["fg3m"], ff["fga"])
    poss = calculate_poss(ff["fga"], ff["oreb"], ff["to"], ff["fta"])
    oreb = calculate_oreb(ff["oreb"], opnt_dreb)
    free_throws = calculate_free_thorows(ff["ftm"], ff["fga"])
    four_factors = (shooting, poss, oreb, free_throws)

    return dict(zip(const.FOUR_FACTORS, four_factors))


def add_trailing_zeros(num: int, n_zeros: int) -> int:
    return int(f"{num}{'0' * n_zeros}")


def get_avg(sum: int, n: int) -> float:
    return round(sum / n, 3)


def save_dataframe_in_file(dataframe: pd.DataFrame, file_name: str) -> None:
    dataframe.to_csv(file_name, index=False)


def calculate_game_id(year: int, game_number: int) -> str:
    return f"002{str(year - 1).zfill(2)}{str(game_number).zfill(5)}"


def generate_games_id(year: int) -> str:
    for game_number in range(1, const.NUM_GAMES + 1):
        yield calculate_game_id(year, game_number)


def get_quartiles(df: pd.DataFrame) -> Tuple[pd.Series, pd.Series, pd.Series]:
    Q1 = df.quantile(0.25)
    Q2 = df.quantile(0.50)
    Q3 = df.quantile(0.75)

    return Q1, Q2, Q3


def remove_outliers(df: pd.DataFrame, target: str) -> pd.DataFrame:
    features = df.drop([target], 1)

    Q1, _, Q3 = get_quartiles(features)
    IQR = Q3 - Q1

    df = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
    return df
