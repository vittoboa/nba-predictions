import const
from utils import remove_outliers

import pickle
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression


def get_matches_data(filename):
    return pd.read_csv(filename)


def remove_first_matches(matches):
    """ remove the first games of each season, it's too early for their data to be relevant """

    for num_season in range(const.NUM_SEASONS):
        beginning_of_season = num_season * const.NUM_GAMES
        matches = matches.drop(
            matches.index[beginning_of_season:(beginning_of_season + const.FIRST_MATCHES)])

    return matches


def get_X_y(matches):
    features = matches.drop([const.TARGET], 1)
    target = matches[const.TARGET]

    X = np.array(features)
    scaler = preprocessing.MinMaxScaler()
    X = scaler.fit_transform(X)
    y = np.array(target)

    return X, y


def create_classifier(X, y):
    print('Creating a classifier...')

    clf = LogisticRegression(solver='saga', penalty='l2', class_weight='balanced')
    clf.fit(X, y)

    return clf


def save_to_file(classifier, filename):
    with open(filename, 'wb') as f:
        pickle.dump(classifier, f)


def save_classifier(filename):
    matches = get_matches_data(const.FILE_MATCHES_DATA)
    matches_relevant = remove_first_matches(matches)
    matches_relevant = remove_outliers(matches_relevant, const.TARGET)
    X, y = get_X_y(matches_relevant)
    clf = create_classifier(X, y)
    save_to_file(clf, filename)
