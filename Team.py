from utils import get_avg


class Team:
    def __init__(self, id, season):
        self.id = id
        self._season = season
        self.reset()

    def reset(self):
        self.matches = 0
        self.shooting = {'off': 0, 'def': 0}
        self.poss = {'off': 0, 'def': 0}
        self.oreb = {'off': 0, 'def': 0}
        self.free_throws = {'off': 0, 'def': 0}

    @property
    def season(self):
        return self._season

    @season.setter
    def season(self, new_season):
        if self._season != new_season:
            self._season = new_season
            self.reset()

    def get_avg_stat(self, stat, side='off'):
        stats = {'shooting': self.shooting, 'poss': self.poss,
                 'oreb': self.oreb, 'free throws': self.free_throws}
        sides = ['off', 'def']

        if stat not in stats:
            raise ValueError("Invalid stat. Expected one of: %s" % stats)
        elif side not in sides:
            raise ValueError("Invalid side. Expected one of: %s" % sides)

        if self.matches == 0:
            stat = 0
        else:
            stat = stats[stat][side]
            stat = get_avg(stat, self.matches)

        return stat

    def update(self, o_stg, d_stg, o_poss, d_poss, o_oreb, d_oreb, o_ft, d_ft):
        self.matches += 1
        self.shooting['off'] += o_stg
        self.shooting['def'] += d_stg
        self.poss['off'] += o_poss
        self.poss['def'] += d_poss
        self.oreb['off'] += o_oreb
        self.oreb['def'] += d_oreb
        self.free_throws['off'] += o_ft
        self.free_throws['def'] += d_ft
