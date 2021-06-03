from bs4 import BeautifulSoup
from selenium import webdriver
import more_itertools
import csv
import os

driver = webdriver.Firefox()
url = "https://www.eloratings.net/"
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')

rows_even = soup.find('div', class_='maindiv').find_all('div', class_='ui-widget-content slick-row even')
rows_odd = soup.find('div', class_='maindiv').find_all('div', class_='ui-widget-content slick-row odd')

rows = list(more_itertools.interleave_longest(rows_even, rows_odd))

ratings = {}
for row in rows:
    team = row.find('div', class_='slick-cell l1 r1 team-cell narrow-layout').find('a').text
    rating = int(row.find('div', class_='slick-cell l2 r2 rating-cell narrow-layout').text)
    ratings[team] = rating

if not os.path.isdir('data'):
    os.mkdir('data')

with open('data/elo_ratings.csv', 'w') as f:
    writer = csv.writer(f)
    for team, rating in ratings.items():
        writer.writerow([team, rating])

driver.quit()
