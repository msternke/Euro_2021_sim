from Group import Group
from Match import Match

class Knockout(object):
    def __init__(self, groups):
        self.groups = groups
        self.round = "Round of 16"

    def play_round_16(self):
        self.determine_thirds_matchups()

        self.build_round_16()

        [match.play_match() for match in self.round_16_matches]

    def play_qfs(self):
        self.round = "Quarterfinals"
        self.build_qfs()

        [match.play_match() for match in self.qf_matches]

    def play_semis(self):
        self.round = "Semifinals"
        self.build_semis()

        [match.play_match() for match in self.semi_matches]

    def play_finals(self):
        self.round = "Finals"
        self.build_finals()

        self.final_match[0].play_match()

    def determine_thirds_matchups(self):
        '''
            Determines matchups in the Round of 16

            The third place finishing teams from four of the six groups
            move on to the knockout round, and the matchups in the round
            are dependent on which four groups they are from.

            See: https://en.wikipedia.org/wiki/UEFA_Euro_2020_knockout_phase
        '''

        index_map = {char: ind for ind, char in enumerate('ABCDEF')}

        #get top four third place finishing teams
        thirds = [group.third for group in self.groups]
        thirds.sort(key=lambda x: (x.group_points, x.goal_diff, x.goals_for), reverse=True)
        thirds_groups = ''.join(sorted([team.group for team in thirds[:4]]))

        if thirds_groups == 'ABCD':
            self.matchups = [index_map[i] for i in 'ADBC']
        elif thirds_groups == 'ABCE':
            self.matchups = [index_map[i] for i in 'AEBC']
        elif thirds_groups == 'ABCF':
            self.matchups = [index_map[i] for i in 'AFBC']
        elif thirds_groups == 'ABDE':
            self.matchups = [index_map[i] for i in 'DEAB']
        elif thirds_groups == 'ABDF':
            self.matchups = [index_map[i] for i in 'DFAB']
        elif thirds_groups == 'ABEF':
            self.matchups = [index_map[i] for i in 'EFBA']
        elif thirds_groups == 'ACDE':
            self.matchups = [index_map[i] for i in 'EDCA']
        elif thirds_groups == 'ACDF':
            self.matchups = [index_map[i] for i in 'FDCA']
        elif thirds_groups == 'ACEF':
            self.matchups = [index_map[i] for i in 'EFCA']
        elif thirds_groups == 'ADEF':
            self.matchups = [index_map[i] for i in 'EFDA']
        elif thirds_groups == 'BCDE':
            self.matchups = [index_map[i] for i in 'EDBC']
        elif thirds_groups == 'BCDF':
            self.matchups = [index_map[i] for i in 'FDCB']
        elif thirds_groups == 'BCEF':
            self.matchups = [index_map[i] for i in 'FECB']
        elif thirds_groups == 'BDEF':
            self.matchups = [index_map[i] for i in 'FEDB']
        elif thirds_groups == 'CDEF':
            self.matchups = [index_map[i] for i in 'FEDC']

    def build_round_16(self):
        '''
            Setting up matches in Round of 16
        '''

        self.determine_thirds_matchups()

        self.round_16_matches = []

        self.round_16_matches.append(Match(self.groups[1].winner, self.groups[self.matchups[0]].third, False))
        self.round_16_matches.append(Match(self.groups[0].winner, self.groups[2].runner_up, False))
        self.round_16_matches.append(Match(self.groups[5].winner, self.groups[self.matchups[3]].third, False))
        self.round_16_matches.append(Match(self.groups[3].runner_up, self.groups[4].runner_up, False))
        self.round_16_matches.append(Match(self.groups[4].winner, self.groups[self.matchups[2]].third, False))
        self.round_16_matches.append(Match(self.groups[3].winner, self.groups[5].runner_up, False))
        self.round_16_matches.append(Match(self.groups[2].winner, self.groups[self.matchups[1]].third, False))
        self.round_16_matches.append(Match(self.groups[0].runner_up, self.groups[1].runner_up, False))

        self.round_16_teams = []
        for match in self.round_16_matches:
            self.round_16_teams.append(match.team1)
            self.round_16_teams.append(match.team2)

    def build_qfs(self):
        '''
            Setting up matches in Quarterfinals
        '''

        self.qf_matches = []

        self.qf_matches.append(Match(self.round_16_matches[0].winner, self.round_16_matches[1].winner, False))
        self.qf_matches.append(Match(self.round_16_matches[2].winner, self.round_16_matches[3].winner, False))
        self.qf_matches.append(Match(self.round_16_matches[4].winner, self.round_16_matches[5].winner, False))
        self.qf_matches.append(Match(self.round_16_matches[6].winner, self.round_16_matches[7].winner, False))

        self.qf_teams = []
        for match in self.qf_matches:
            self.qf_teams.append(match.team1)
            self.qf_teams.append(match.team2)

    def build_semis(self):
        '''
            Setting up matches in Semifinals
        '''

        self.semi_matches = []

        self.semi_matches.append(Match(self.qf_matches[0].winner, self.qf_matches[1].winner, False))
        self.semi_matches.append(Match(self.qf_matches[2].winner, self.qf_matches[3].winner, False))

        self.semi_teams = []
        for match in self.semi_matches:
            self.semi_teams.append(match.team1)
            self.semi_teams.append(match.team2)

    def build_finals(self):
        '''
            Setting up Finals match
        '''

        self.final_match = [Match(self.semi_matches[0].winner, self.semi_matches[1].winner, False)]

        self.final_teams = [self.final_match[0].team1, self.final_match[0].team2]

    def print_matches(self, matches):
        '''
            Prints results of finals match
        '''

        if self.round == 'Finals':
            print(f"***** {self.round}!!! ******")
        else:
            print(f"***** {self.round} matches ******")

        for m in matches:
            if m.penalties:
                print(f"{m.winner.name} beats {m.loser.name} in penalties!")
            else:
                print(f"{m.winner.name} beats {m.loser.name}!")
        print()
