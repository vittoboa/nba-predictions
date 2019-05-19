import const

import pickle
import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


def get_matches_data(filename):
    return pd.read_csv(filename)

def remove_first_matches(matches):
    """ remove the first games of each season, it's too early for their data to be relevant """

    for num_season in range(const.NUM_SEASONS):
        beginning_of_season = num_season * const.NUM_GAMES
        matches = matches.drop(
            matches.index[beginning_of_season:(beginning_of_season + const.FIRST_MATCHES)])

    return matches

def merge_related_features(matches):
    new_matches = pd.DataFrame()
    new_matches["win diff"] = matches["home win percentage"] - matches["away win percentage"]
    new_matches["last 5 wins diff"] = matches["home last 5 wins"] - matches["away last 5 wins"]
    new_matches["points diff"] = matches["home avg points"] - matches["away avg points"]
    new_matches["last 5 points diff"] = matches["home last 5 points"] - matches["away last 5 points"]
    new_matches["winner"] = matches["winner"]
    return new_matches

def get_X_y(matches):
    forecast_column = "winner"
    X = np.array(matches.drop([forecast_column], 1))
    y = np.array(matches[forecast_column])

    return X, y

def create_classifier(X, y):
    print('Creating a classifier...')
    clf = QuadraticDiscriminantAnalysis()
    clf.fit(X, y)

    return clf

def save_to_file(classifier, filename):
    with open(filename, 'wb') as f:
        pickle.dump(classifier, f)

def save_classifier(filename):
    matches = get_matches_data(const.FILE_MATCHES_DATA)
    relevant_matches = remove_first_matches(matches)
    relevant_matches = merge_related_features(relevant_matches)
    X, y = get_X_y(relevant_matches)
    clf = create_classifier(X, y)
    save_to_file(clf, filename)
