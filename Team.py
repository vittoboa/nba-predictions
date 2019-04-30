class Team:
    def __init__(self, id, season):
        self.id = id
        self._season = season
        self.reset()

    def reset(self):
        self.matches = 0
        self.wins = 0
        self.points = 0
        self.plus_minus = 0

    @property
    def season(self):
        return self._season
    
    @season.setter
    def season(self, new_season):
        if self._season != new_season:
            self._season = new_season
            self.reset()
    
    def get_win_percentage(self):
        return round(self.wins / self.matches, 3)
    
    def get_avg_points(self):
        return round(self.points / self.matches)

    def update(self, points, points_opponents):
        is_winner = points > points_opponents
        self.wins += is_winner
        self.matches += 1
        self.points += points
        self.plus_minus += (points - points_opponents)

