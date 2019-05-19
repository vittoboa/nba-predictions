import os
import const
import pickle

import data_collection
import create_classifier


def retrive_classifier():
    pickle_in = open(const.FILE_CLASSIFIER, 'rb')
    classifier = pickle.load(pickle_in)
    return classifier

def predict(classifier, data):
    print('Computing...')
    return classifier.predict([data])[0]

def get_winner_name(prediction, home_name, away_name):
    home, away = 0, 1
    winner = home_name if prediction == home else away_name
    return winner

def ask_team_name(court):
    return input(court + ' team name: ')

def ask_win_percentage(court):
    return float(input(court + ' team win percentage: '))

def ask_avg_points(court):
    return float(input(court + ' team average points per game: '))

def ask_last_5_wins(court):
    return float(input(court + ' team wins in the last 5 matches: '))

def ask_last_5_points(court):
    return float(input(court + ' team points in the last 5 matches: '))

def get_team_data(court):
    team_data = []
    team_data.append(ask_win_percentage(court))
    team_data.append(ask_last_5_wins(court))
    team_data.append(ask_avg_points(court))
    team_data.append(ask_last_5_points(court))

    return team_data

def main():
    """ ask the user about the teams data """
    print('Enter the following informations about the match that needs to be predicted.')
    team_home_name, team_home_data = ask_team_name('Home'), get_team_data('Home')
    team_away_name, team_away_data = ask_team_name('Away'), get_team_data('Away')
    teams_data = [home - away for home, away in zip(team_home_data, team_away_data)]

    """ if a classifier has been saved retrive it, else create a new one """
    if not os.path.exists('./' + const.FILE_CLASSIFIER):
        # create a classifier
        if not os.path.exists('./' + const.FILE_MATCHES_DATA):
            # save matches timeline if doesn't exist
            data_collection.save_matches_timeline(const.FILE_MATCHES_DATA)
        create_classifier.save_classifier(const.FILE_CLASSIFIER)
    clf = retrive_classifier()

    """ predict the winner """
    prediction = predict(clf, teams_data)
    winner = get_winner_name(prediction, team_home_name, team_away_name)
    print("The winner is: " + winner)


if __name__ == '__main__':
    main()
