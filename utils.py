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


def save_dataframe_in_file(dataframe, file_name):
    dataframe.to_csv(file_name, index=False)


def add_digits(num, digits):
    num_digits = sum(1 for _ in str(num))
    return ''.join('0' for _ in range(digits - num_digits)) + str(num)
