import numpy as np
import scipy.stats as ss

class Match(object):
    def __init__(self, team1, team2, group_stage_flag):
        self.team1 = team1
        self.team2 = team2
        self.group_stage_flag = group_stage_flag

        self.eloK = 50
        self.elo_match_model()

        self.penalties = False

    def elo_match_model(self):
        # log( mu ) = alpha + beta*(elo_diff/100)
        self.alpha = 0.1727
        self.beta = 0.107132

    def play_match(self):
        elo_diff = self.team1.elo - self.team2.elo

        mu1 = np.exp(self.alpha + self.beta*(elo_diff/100))
        mu2 = np.exp(self.alpha - self.beta*(elo_diff/100))

        goals1 = ss.poisson.rvs(mu1)
        goals2 = ss.poisson.rvs(mu2)
        goal_diff = goals1 - goals2

        if goal_diff > 0:
            self.winner = self.team1
            self.loser = self.team2
        elif goal_diff < 0:
            self.winner = self.team2
            self.loser = self.team1

        self.update_team_stats(goals1, goals2)
        self.update_elo_ratings(goal_diff, elo_diff)

        if not self.group_stage_flag and goal_diff == 0:
            self.penalties = True
            self.penalty_shootout()

    def update_team_stats(self, goals_team1, goals_team2):
        self.team1.matches += 1
        self.team2.matches += 1

        self.team1.goals_for += goals_team1
        self.team1.goals_against += goals_team2
        self.team1.goal_diff += goals_team1 - goals_team2

        self.team2.goals_for += goals_team2
        self.team2.goals_against += goals_team1
        self.team2.goal_diff += goals_team2 - goals_team1

        if self.group_stage_flag:
            if goals_team1 > goals_team1:
                self.team1.group_points += 3
            elif goals_team2 > goals_team1:
                self.team2.group_points += 3
            else:
                self.team1.group_points += 1
                self.team2.group_points += 1

    def update_elo_ratings(self, goal_diff, elo_diff):
        #scaling factor for goal difference
        if np.abs(goal_diff) > 2:
            K = self.eloK * (1.75 + (np.abs(goal_diff) - 3) / 8)
        elif np.abs(goal_diff) == 2:
            K = self.eloK * 1.5
        else:
            K = self.eloK

        #win/loss/draw result
        if goal_diff > 0:
            W = 1
        elif goal_diff < 0:
            W = 0
        else:
            W = 0.5

        #win expectancy eqn
        We = 1 / (10 ** (-1 * elo_diff/400) + 1)

        #update team elo ratings
        self.team1.elo += round(K * (W - We))
        self.team2.elo -= round(K * (W - We))

    def penalty_shootout(self, n_kicks = 5):
        avg_pk_success = 0.75

        team1_goals = ss.binom.rvs(n_kicks, avg_pk_success)
        team2_goals = ss.binom.rvs(n_kicks, avg_pk_success)

        while team1_goals == team2_goals:
            team1_goals += ss.bernoulli.rvs(avg_pk_success)
            team2_goals += ss.bernoulli.rvs(avg_pk_success)

        if team1_goals > team2_goals:
            self.winner = self.team1
            self.loser = self.team2
        else:
            self.winner = self.team2
            self.loser = self.team1

    def __repr__(self):
        print(f"")
