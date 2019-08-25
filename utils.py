def calculate_shooting(fgm, fg3m, fga):
    """ effective field goal """
    return (fgm + fg3m/2) / fga


def calculate_poss(fga, oreb, to, fta):
    """ offensive possession """
    return fga - oreb + to + (0.4 * fta)


def calculate_oreb(oreb, opponent_dreb):
    """ offensive rebounding """
    return oreb / (oreb + opponent_dreb)


def calculate_free_thorows(ftm, fga):
    """ getting to the foul line """
    return ftm / fga


def calculate_four_factors(four_factors_data, opnt_dreb):
    ffd = four_factors_data

    shooting = calculate_shooting(ffd["fgm"], ffd["fg3m"], ffd["fga"])
    poss = calculate_poss(ffd["fga"], ffd["oreb"], ffd["to"], ffd["fta"])
    oreb = calculate_oreb(ffd["oreb"], opnt_dreb)
    free_throws = calculate_free_thorows(ffd["ftm"], ffd["fga"])

    return shooting, poss, oreb, free_throws


def get_avg(sum, n):
    return round(sum / n, 3)


def save_dataframe_in_file(dataframe, file_name):
    dataframe.to_csv(file_name, index=False)


def add_digits(num, digits):
    num_digits = sum(1 for _ in str(num))
    return ''.join('0' for _ in range(digits - num_digits)) + str(num)


def get_quartiles(dataframe):
    Q1 = dataframe.quantile(0.25)
    Q2 = dataframe.quantile(0.50)
    Q3 = dataframe.quantile(0.75)

    return Q1, Q2, Q3


def remove_outliers(df, target):
    features = df.drop([target], 1)

    Q1, _, Q3 = get_quartiles(features)
    IQR = Q3 - Q1

    df = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
    return df
