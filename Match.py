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
        '''
            Defines model coefficients to predict expected goals based on
            Elo rating different between teams

            Determined from historical_goals_analysis
        '''

        # log(labmda) = alpha + beta*(elo_diff/100)
        self.alpha = 0.1727
        self.beta = 0.107132

    def play_match(self):
        '''
            Simulates match
        '''

        elo_diff = self.team1.elo - self.team2.elo

        #Determine expected goal value for each team
        mu1 = np.exp(self.alpha + self.beta*(elo_diff/100))
        mu2 = np.exp(self.alpha - self.beta*(elo_diff/100))

        #Get goals scored by each team by random draws from Poisson ditributions
        goals1 = ss.poisson.rvs(mu1)
        goals2 = ss.poisson.rvs(mu2)
        goal_diff = goals1 - goals2

        #Determine match winner
        if goal_diff > 0:
            self.winner = self.team1
            self.loser = self.team2
        elif goal_diff < 0:
            self.winner = self.team2
            self.loser = self.team1

        #Update team stats and Elo ratings based on results of match
        self.update_team_stats(goals1, goals2)
        self.update_elo_ratings(goal_diff, elo_diff)

        #Go to a penalty shootout if score tied and in Knockout phase
        if not self.group_stage_flag and goal_diff == 0:
            self.penalties = True
            self.penalty_shootout()

    def update_team_stats(self, goals_team1, goals_team2):
        #Update team stats
        self.team1.matches += 1
        self.team2.matches += 1

        self.team1.goals_for += goals_team1
        self.team1.goals_against += goals_team2
        self.team1.goal_diff += goals_team1 - goals_team2

        self.team2.goals_for += goals_team2
        self.team2.goals_against += goals_team1
        self.team2.goal_diff += goals_team2 - goals_team1

        #Update team group points
        if self.group_stage_flag:
            if goals_team1 > goals_team1:
                self.team1.group_points += 3
            elif goals_team2 > goals_team1:
                self.team2.group_points += 3
            else:
                self.team1.group_points += 1
                self.team2.group_points += 1

    def update_elo_ratings(self, goal_diff, elo_diff):
        #Scaling factor for goal difference of match
        if np.abs(goal_diff) > 2:
            K = self.eloK * (1.75 + (np.abs(goal_diff) - 3) / 8)
        elif np.abs(goal_diff) == 2:
            K = self.eloK * 1.5
        else:
            K = self.eloK

        #Win/loss/draw result
        if goal_diff > 0:
            W = 1
        elif goal_diff < 0:
            W = 0
        else:
            W = 0.5

        #Expected win equation
        We = 1 / (10 ** (-1 * elo_diff/400) + 1)

        #Update team elo ratings
        self.team1.elo += round(K * (W - We))
        self.team2.elo -= round(K * (W - We))

    def penalty_shootout(self, n_kicks = 5):
        '''
            Run penalty shootout

            Modeled as random draw from binomial distribution with a success
            rate determined by average success of penalties

            If penalties tied after 5 shots, keep shooting (random draws from
            Bernoulli distribution) until scores not tied.

            For now each team has same success rate, may change in future
        '''
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
