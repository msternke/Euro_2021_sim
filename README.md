# UEFA Euro 2021 sims

## Overview
After a year of waiting, the 2020 UEFA Euro championships are here! In anticipation for the tournament, I thought it would be fun to determine each teams' chance of winning. To do this, I have used the Elo rating system and analyzed historical match results to develop a probabilistic model for match outcomes. I've then built a Monte Carlo simulation framework to simulate the entirety of the tournament (both the Group stage and the Knockout rounds) to determine who will win. By running these simulations many, many times, we can determine each teams' probability of winning determined by the model.

## Running the simulations
The simulations can be run using the Euro_2021_sim.py script. To run the script, you will need to install pandas, numpy, scipy, and matplotlib.

## Preview of results
I'll be writing a series of posts about my approach to the simulations and the results at [https://msternke.github.io/](https://msternke.github.io/). Check them out there! However, a quick plot of each teams' chances of winning the tournament is below. Looks like I'm betting on Belgium!

![Win plot](/figures/win_prob_bar_chart.png)
