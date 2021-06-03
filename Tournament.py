from Group import Group
from Knockout import Knockout

class Tournament(object):
    def __init__(self, teams, group_names):
        self.teams = teams
        self.group_names = group_names

    def play_tournament(self):
        self.groups = []
        for group_name in self.group_names:
            group_teams = [team for team in self.teams if team.group == group_name]
            self.groups.append(Group(group_name, group_teams))

        [group.play_group() for group in self.groups]

        self.knockout = Knockout(self.groups)

        self.knockout.play_round_16()
        #self.knockout.print_matches(self.knockout.round_16_matches)
        self.knockout.play_qfs()
        #self.knockout.print_matches(self.knockout.qf_matches)
        self.knockout.play_semis()
        #self.knockout.print_matches(self.knockout.semi_matches)
        self.knockout.play_finals()
        #self.knockout.print_matches(self.knockout.final_match)

        self.tournament_winner = self.knockout.final_match[0].winner
