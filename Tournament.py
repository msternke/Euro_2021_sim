from Group import Group
from Knockout import Knockout

class Tournament(object):
    def __init__(self, teams, group_names):
        self.teams = teams
        self.group_names = group_names

    def play_tournament(self):
        '''
            Runs simulation to play the entire tournament
        '''

        #Set up groups
        self.groups = []
        for group_name in self.group_names:
            group_teams = [team for team in self.teams if team.group == group_name]
            self.groups.append(Group(group_name, group_teams))

        #Play group round games
        [group.play_group() for group in self.groups]

        #Set up Knockout round
        self.knockout = Knockout(self.groups)

        #Play all knockout round games
        self.knockout.play_round_16()
        self.knockout.play_qfs()
        self.knockout.play_semis()
        self.knockout.play_finals()

        #Set tournament winner
        self.tournament_winner = self.knockout.final_match[0].winner
