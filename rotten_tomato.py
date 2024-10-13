import urllib.request as requests
from bs4 import BeautifulSoup
import pandas as pd
import os
os.chdir('C:\\Users\\IDEAL\\Desktop')

url = 'https://www.rottentomatoes.com/'

# Make the request
response = requests.urlopen(url)

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(response, 'html.parser')

# Find all the movie items (assuming this is correct, based on your initial code)
movie_carousels = soup.find_all('tiles-carousel-responsive-item-deprecated')

# Prepare lists for movie names and their source
names = []
movie_urls = []
similar_movies = []

for movie in movie_carousels:
    name_tag = movie.find('a').find('span')
    if name_tag:
        names.append(name_tag.string)
    movie_url = url + movie.find('a').get('href')
    movie_urls.append(movie_url)

def get_similar_movies(movie_url):
    # Fetch the HTML of the given movie URL
    html = requests.urlopen(movie_url).read()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the section containing similar movies
    more_like_this = soup.find('section', {'aria-labelledby': 'more-like-this-label', 'class': 'more-like-this'})

    # Extract the titles of similar movies
    similar_movies = more_like_this.find_all('rt-link', {'slot': 'title'})

    # Create a list to store the names of similar movies
    lst = []
    for movie in similar_movies:
        lst.append(movie.text.strip())  # Extract and clean the text of each movie title

    return ', '.join(lst)  # Return the list of similar movie names

for movie_url in movie_urls:
    try:
        text =  get_similar_movies(movie_url)
        similar_movies.append(text)
    except:
        similar_movies.append('')

# Create a DataFrame from the lists
df = pd.DataFrame({
    'Movie Name': names,
    'URL' : movie_urls,
    'More Like This' : similar_movies
})

# Print DataFrame to CSV
df.to_csv('movies.csv', index=False)

print("Movies have been saved to 'movies.csv'.")
