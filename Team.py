class Team(object):
    def __init__(self, name, group, elo):
        self.name = name
        self.group = group
        self.elo = elo

        self.matches = 0
        self.goals_for = 0
        self.goals_against = 0
        self.goal_diff = 0

        self.group_points = 0
        self.group_finish = 0

    def __repr__(self):
        return f"{self.name} {self.group} {self.group_points}"
