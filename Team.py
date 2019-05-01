import collections


def get_avg(sum, n):
    return sum / n


class Team:
    def __init__(self, id, season):
        self.id = id
        self._season = season
        self.reset()

    def reset(self):
        self.matches = 0
        self.wins = 0
        self.points = 0
        self.last_5_wins = collections.deque(maxlen=5)
        self.last_5_points = collections.deque(maxlen=5)

    @property
    def season(self):
        return self._season
    
    @season.setter
    def season(self, new_season):
        if self._season != new_season:
            self._season = new_season
            self.reset()
    
    def get_win_percentage(self):
        return 0 if self.matches == 0 else round(get_avg(self.wins, self.matches), 3)
    
    def get_avg_points(self):
        return 0 if self.matches == 0 else round(get_avg(self.points, self.matches))

    def get_last_5_wins(self):
        return sum(self.last_5_wins)
    
    def get_last_5_points(self):
        return sum(self.last_5_points)

    def update(self, points, points_opponents):
        is_winner = points > points_opponents
        self.wins += is_winner
        self.matches += 1
        self.points += points
        self.last_5_wins.append(is_winner)
        self.last_5_points.append(points)
