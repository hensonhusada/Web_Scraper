import requests
from requests import get
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

#initializing empty lists for data
titles = []
years = []
time = []
imdb_ratings = []
metascore = []
votes = []
us_gross = []

#fetching web html with beautiful soup
headers ={"Accept-Language" : "en-US, en;q=0.5"}
base_url = "https://www.imdb.com"
second_url = "/search/title/?groups=top_1000&ref_=adv_prv"

for i in range(0, 20):
    url = base_url+second_url
    results = requests.get(url, headers=headers)
    soup = bs(results.text, "html.parser")
    try:
        second_url = soup.find('a', class_='lister-page-next').get('href')
    except:
        print('No More url')
    movie_div = soup.find_all('div', class_='lister-item mode-advanced')
    for container in movie_div:
        #name
        name = container.h3.a.text
        titles.append(name)
        
        #year
        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)
        
        #runtime
        runtime = container.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else '-'
        time.append(runtime)
        
        #IMDB rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)
        
        #metascore
        meta = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
        metascore.append(meta)
        
        #votes and grosses
        nv = container.find_all('span', attrs={'name':'nv'})
        vote = nv[0].text
        votes.append(vote)
        grosses = nv[1].text if len(nv)>1 else '-'
        us_gross.append(grosses)
    
movies = pd.DataFrame({
'movie':titles,
'year':years,
'timeMin':time,
'imdb':imdb_ratings,
'metascore':metascore,
'votes':votes,
'us_grossMillions':us_gross,
})

#cleaning up the data
movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
movies['metascore'] = pd.to_numeric(movies['metascore'], errors = 'coerce')
movies['votes'] = movies['votes'].str.replace(',','').astype(int)
movies['us_grossMillions'] = movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['us_grossMillions'] = pd.to_numeric(movies['us_grossMillions'], errors = 'coerce')
print(movies)
# print(movies.dtypes)

#export to csv file
movies.to_csv('movies.csv')    