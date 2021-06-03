from itertools import combinations

from Match import Match

class Group(object):
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams

    def play_group(self):
        #self.matches = [Match(matchup[0], matchup[1], True) for matchup in combinations(self.teams, 2)]
        self.matches = [
            Match(self.teams[0], self.teams[1], True),
            Match(self.teams[2], self.teams[3], True),
            Match(self.teams[0], self.teams[2], True),
            Match(self.teams[1], self.teams[3], True),
            Match(self.teams[0], self.teams[3], True),
            Match(self.teams[1], self.teams[2], True)
        ]


        [match.play_match() for match in self.matches]

        self.group_table()

    def group_table(self):
        self.table = sorted(self.teams, key=lambda x: (x.group_points, x.goal_diff, x.goals_for), reverse=True)

        self.winner = self.table[0]
        self.runner_up = self.table[1]
        self.third = self.table[2]

        for i, team in enumerate(self.table):
            team.group_finish = i + 1

    def print_table(self): # print the group tables
        print(f"***** GROUP {self.name} Table ******")
        template = "{0:14}{1:3}{2:3}{3:3}{4:3}{5:3}"
        print(template.format("Team", " Pl", " GF", " GA", " GD", " Pt"))
        print('-'*29)
        for t in self.table:
            row = [t.matches,t.goals_for,t.goals_against,t.goal_diff,t.group_points]
            print(template.format( t.name, *row))
        print('-'*29)
