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


def get_four_factors(four_factors: Dict[str, float], opnt_dreb: float) -> Dict[str, float]:
    ff = four_factors

    shooting = calculate_shooting(ff["fgm"], ff["fg3m"], ff["fga"])
    poss = calculate_poss(ff["fga"], ff["oreb"], ff["to"], ff["fta"])
    oreb = calculate_oreb(ff["oreb"], opnt_dreb)
    free_throws = calculate_free_thorows(ff["ftm"], ff["fga"])
    four_factors = (shooting, poss, oreb, free_throws)

    return dict(zip(const.FOUR_FACTORS, four_factors))


def get_avg(sum: int, n: int) -> float:
    return round(sum / n, 3)


def save_dataframe_in_file(dataframe: pd.DataFrame, file_name: str) -> None:
    dataframe.to_csv(file_name, index=False)


def calculate_game_id(year, game_number):
    return "002" + str(year - 1).zfill(2) + str(game_number).zfill(5)


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
