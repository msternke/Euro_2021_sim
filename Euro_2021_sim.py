from Team import Team
from Tournament import Tournament

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from collections import defaultdict

#Simulation parameters
Nsims = 10000
np.random.seed(42)

#Importing data
team_data = pd.read_csv('data/euro_teams_data.csv')
groups = sorted(np.unique(team_data['Group']))

#Start simulations
sims = []

finals_wins = defaultdict(int)

for i in range(Nsims):

    teams = [Team(row['Country'], row['Group'], row['Elo']) for ix, row in team_data.iterrows()]

    t = Tournament(teams, groups)
    t.play_tournament()

    finals_wins[t.tournament_winner.name] += 1 / Nsims

plt.bar(*zip(*sorted(finals_wins.items(), key=lambda x: x[1], reverse=True)))
plt.xticks(rotation=90)
plt.xlabel('Team')
plt.ylabel('Win probability')
plt.savefig('figures/win_prob_bar_chart.png', dpi=300, bbox_inches='tight')
plt.close()
