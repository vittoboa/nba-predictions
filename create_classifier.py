import const

import pandas as pd


def get_matches_data(filename):
    return pd.read_csv(filename)

def remove_first_matches(matches):
    """ remove the first games of each season, it's too early for their data to be relevant """

    for num_season in range(const.NUM_SEASONS):
        beginning_of_season = num_season * const.NUM_GAMES
        matches = matches.drop(
            matches.index[beginning_of_season:(beginning_of_season + const.FIRST_MATCHES)])

    return matches


if __name__ == '__main__':
    matches = get_matches_data("matches.csv")
    relevant_matches = remove_first_matches(matches)
