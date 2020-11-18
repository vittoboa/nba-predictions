import os
from itertools import chain
import const
import pickle
from data_collection import save_matches_timeline
from create_classifier import save_classifier
from utils import get_four_factors


def retrive_classifier():
    pickle_in = open(const.FILE_CLASSIFIER, 'rb')
    classifier = pickle.load(pickle_in)
    return classifier


def predict(classifier, data):
    print('Computing...')
    return classifier.predict(data)[0]


def get_winner_name(prediction, home_name, away_name):
    home, away = 0, 1
    winner = home_name if prediction == home else away_name
    return winner


def ask_team_name(court):
    return input(court + ' team name: ')


def ask_stat(stat, court, is_opnt=False):
    return float(input(f"{stat} ({court} team's {'opponent ' if is_opnt else ''}stats): "))


def ask_teams_data(court):
    data_team = {}
    data_opponent = {}

    data_team["avg win"] = ask_stat("avg win percentage", court)
    data_team["pts"] = ask_stat("points", court)
    data_opponent["pts"] = ask_stat("points", court, is_opnt=True)
    data_team["fgm"] = ask_stat("field goals", court)
    data_opponent["fgm"] = ask_stat("field goals", court, is_opnt=True)
    data_team["fg3m"] = ask_stat("3-point field goals", court)
    data_opponent["fg3m"] = ask_stat("3-point field goals", court, is_opnt=True)
    data_team["fga"] = ask_stat("field goal attempts", court)
    data_opponent["fga"] = ask_stat("field goal attempts", court, is_opnt=True)
    data_team["oreb"] = ask_stat("offensive rebounds", court)
    data_opponent["oreb"] = ask_stat("offensive rebounds", court, is_opnt=True)
    data_team["dreb"] = ask_stat("defensive rebounds", court)
    data_opponent["dreb"] = ask_stat("defensive rebounds", court, is_opnt=True)
    data_team["to"] = ask_stat("turnovers", court)
    data_opponent["to"] = ask_stat("turnovers", court, is_opnt=True)
    data_team["fta"] = ask_stat("free throw attempts", court)
    data_opponent["fta"] = ask_stat("free throw attempts", court, is_opnt=True)
    data_team["ftm"] = ask_stat("free throws", court)
    data_opponent["ftm"] = ask_stat("free throws", court, is_opnt=True)

    return data_team, data_opponent


def get_teams_data(home, away):
    home_data, home_data_opponent = ask_teams_data(home)
    away_data, away_data_opponent = ask_teams_data(away)
    home_avg_win, away_avg_win = home_data["avg win"], away_data["avg win"]
    home_pts, home_pts_opponent = home_data["pts"], home_data_opponent["pts"]
    away_pts, away_pts_opponent = away_data["pts"], away_data_opponent["pts"]
    home_four_factors = get_four_factors(home_data, away_data["dreb"])
    home_four_factors_opponent = get_four_factors(home_data_opponent, away_data_opponent["dreb"])
    away_four_factors = get_four_factors(away_data, home_data["dreb"])
    away_four_factors_opponent = get_four_factors(away_data_opponent, home_data_opponent["dreb"])

    home_data_final = chain([home_avg_win, home_pts], home_four_factors.values(),
                            [home_pts_opponent], home_four_factors_opponent.values())

    away_data_final = chain([away_avg_win, away_pts], away_four_factors.values(),
                            [away_pts_opponent], away_four_factors_opponent.values())

    return list(chain(home_data_final, away_data_final))


def main():
    """ ask the user about the teams data """
    print('Enter the following informations about the match that needs to be predicted.')
    home_name, away_name = ask_team_name("Home"), ask_team_name("Away")
    teams_data = get_teams_data(home_name, away_name)

    """ if a classifier has been saved retrive it, else create a new one """
    if not os.path.exists('./' + const.FILE_CLASSIFIER):
        # create a classifier
        if not os.path.exists('./' + const.FILE_RAW):
            # save matches timeline if doesn't exist
            save_matches_timeline(const.FILE_RAW)
        save_classifier(const.FILE_CLASSIFIER)
    clf = retrive_classifier()

    """ predict the winner """
    prediction = predict(clf, [teams_data])
    winner = get_winner_name(prediction, home_name, away_name)
    print("The winner is: " + winner)


if __name__ == '__main__':
    main()
