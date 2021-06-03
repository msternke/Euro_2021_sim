from bs4 import BeautifulSoup
from selenium import webdriver
import more_itertools
import datetime as dt
import time
import pandas as pd

def parse_row(row):
    date_string_raw = list(row.find('div', class_='slick-cell l0 r0 match-cell').stripped_strings)

    if len(date_string_raw) == 1:
        date_string = date_string_raw
    else:
        date_string = date_string_raw[0].split() + [date_string_raw[1]]

    if len(date_string) == 3:
        row_date = dt.datetime.strptime(' '.join(date_string), '%B %d %Y')
    if len(date_string) == 2:
        row_date = dt.datetime.strptime(' '.join([date_string[0], '1', date_string[1]]), '%B %d %Y')
    if len(date_string) == 1:
        row_date = dt.datetime.strptime(' '.join(['January', '1', date_string[0]]), '%B %d %Y')

    teams = row.find_all('a')
    team1 = teams[0].text
    team2 = teams[1].text

    ratings = list(row.find('div', class_='slick-cell l5 r5 score-cell').stripped_strings)
    team1_rating = int(ratings[0])
    team2_rating = int(ratings[1])

    return row_date, team1, team1_rating, team2, team2_rating

date = []
team = []
rating = []

for year in range(1980, 2022):
    driver = webdriver.Firefox()
    url = f"https://www.eloratings.net/{year}_results"
    driver.get(url)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    rows_even = soup.find('div', class_='maindiv').find_all('div', class_='ui-widget-content slick-row even')
    rows_odd = soup.find('div', class_='maindiv').find_all('div', class_='ui-widget-content slick-row odd')
    rows = list(more_itertools.interleave_longest(rows_even, rows_odd))

    for row in rows:
        row_date, team1, team1_rating, team2, team2_rating = parse_row(row)

        date.append(row_date)
        team.append(team1)
        rating.append(team1_rating)

        date.append(row_date)
        team.append(team2)
        rating.append(team2_rating)

    driver.close()
    print(f"Finished {year}")

ratings = pd.DataFrame({'date': date, 'team': team, 'rating': rating})

ratings.to_csv('data/team_elos_over_time.csv')
