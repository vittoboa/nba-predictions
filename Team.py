from utils import get_avg, get_four_factors


class Team:
    def __init__(self, id, season):
        self.id = id
        self._season = season
        self.reset()

    def reset(self):
        self.matches = 0
        self.win = 0
        self.pts = {'off': 0, 'def': 0}
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

    def get_avg_stat(self, stat, side=None):
        stats = {'win': self.win, 'pts': self.pts,
                 'shooting': self.shooting, 'poss': self.poss,
                 'oreb': self.oreb, 'free throws': self.free_throws}
        sides = ['off', 'def', None]

        if stat not in stats:
            raise ValueError("Invalid stat. Expected one of: %s" % stats)
        elif side not in sides:
            raise ValueError("Invalid side. Expected one of: %s" % sides)

        if self.matches == 0:
            stat = 0
        else:
            stat = stats[stat] if side is None else stats[stat][side]
            stat = get_avg(stat, self.matches)

        return stat

    def update(self, own_data, opnt_data):
        own_four_factors = get_four_factors(own_data, opnt_data["dreb"])
        opnt_four_factors = get_four_factors(opnt_data, own_data["dreb"])

        self.matches += 1
        self.win += 1 if own_data['pts'] > opnt_data['pts'] else 0
        self.pts['off'] += own_data['pts']
        self.pts['def'] += opnt_data['pts']
        self.shooting['off'] += own_four_factors['shooting']
        self.shooting['def'] += opnt_four_factors['shooting']
        self.poss['off'] += own_four_factors['poss']
        self.poss['def'] += opnt_four_factors['poss']
        self.oreb['off'] += own_four_factors['oreb']
        self.oreb['def'] += opnt_four_factors['oreb']
        self.free_throws['off'] += own_four_factors['free throws']
        self.free_throws['def'] += opnt_four_factors['free throws']
