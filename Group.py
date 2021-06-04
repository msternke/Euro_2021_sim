from itertools import combinations

from Match import Match

class Group(object):
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams

    def play_group(self):
        '''
            Runs the simluations for all games in the group
        '''

        #Instantiate all games in the group
        self.matches = [
            Match(self.teams[0], self.teams[1], True),
            Match(self.teams[2], self.teams[3], True),
            Match(self.teams[0], self.teams[2], True),
            Match(self.teams[1], self.teams[3], True),
            Match(self.teams[0], self.teams[3], True),
            Match(self.teams[1], self.teams[2], True)
        ]

        #Play all games
        [match.play_match() for match in self.matches]

        #Formulate group table
        self.group_table()

    def group_table(self):
        '''
            Formulates group table from game results
        '''

        #Sort teams by points, break ties by goal differential
        #Break further ties by goals for
        self.table = sorted(self.teams, \
            key=lambda x: (x.group_points, x.goal_diff, x.goals_for), reverse=True)

        #Get winner, runner up, and third place finisher
        self.winner = self.table[0]
        self.runner_up = self.table[1]
        self.third = self.table[2]

        #Save where each team finishes in the group
        for i, team in enumerate(self.table):
            team.group_finish = i + 1

    def print_table(self):
        '''
            Prints group table to terminal
        '''

        print(f"***** GROUP {self.name} Table ******")
        template = "{0:14}{1:3}{2:3}{3:3}{4:3}{5:3}"
        print(template.format("Team", " Pl", " GF", " GA", " GD", " Pt"))
        print('-'*29)
        for t in self.table:
            row = [t.matches,t.goals_for,t.goals_against,t.goal_diff,t.group_points]
            print(template.format( t.name, *row))
        print('-'*29)
