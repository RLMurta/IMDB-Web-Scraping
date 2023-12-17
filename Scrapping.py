import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
from Actor import Actor
from Movie import Movie

class Scrapping:
    
    def __init__(self) -> None:
        self.all_time_movies = []
        self.all_time_movies_names = []

    # Checks if a movie name is in the all time movies list
    def is_in_all_time_movies(self, movie):
        return movie.name in self.all_time_movies_names

    # Adds a movie to the all time movies list and its name to the all time movies names list
    def add_to_all_time_movies(self, movie):
        self.all_time_movies.append(movie)
        self.all_time_movies_names.append(movie.name)

    # Gets the html from the page of a given link
    def get_webpage(self,link):
        # Requests with a user agent to avoid getting blocked
        page = requests.get(link, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        return BeautifulSoup(page.text,'html.parser')

    # Gets all the actors and actresses from the imdb top 50 actors/actresses page
    def get_actors(self):
        actor_list = []
        # Gets the all actors/actresses page
        soup = self.get_webpage('https://www.imdb.com/list/ls053501318/')
        list_of_actors = soup.find('div', class_="lister-list")
        for row in list_of_actors.find_all('div'):
            # Gets the div where the actor/actress name, about and link to its page is present
            div = row.find('div', class_="lister-item-content")
            if div is not None:
                h3 = div.find('h3', class_="lister-item-header")
                name = h3.find_all('a')[0].find(text=True).replace("\n", "")
                link = 'https://www.imdb.com'+ h3.find_all('a',href=True)[0]['href']
                about = div.find_all('p')[1].find_all(text=True)
                about = ''.join(about)
                # Gets the actor page
                actor_page_soup = self.get_webpage(link)
                all_time_movies = self.get_movies(actor_page_soup)
                awards = self.get_actor_data(actor_page_soup)
                actor = Actor(name, about,link, all_time_movies, awards)
                actor_list.append(actor)
                print(actor)
        return actor_list

    # Gets the movie data from the movie page
    def get_movies(self,soup):
        movies_list = []
        list_of_movies = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-between ipc-metadata-list--base")
        for row in list_of_movies.find_all('li'):
            enclosure_div = row.find('div', class_="ipc-metadata-list-summary-item__c")
            if enclosure_div is not None:
                data_div = enclosure_div.find('div', class_="ipc-metadata-list-summary-item__tc")
                name = data_div.find('a', class_="ipc-metadata-list-summary-item__t").find(text=True).replace("\n", "")
                link = 'https://www.imdb.com'+ data_div.find_all('a',href=True)[0]['href']
                movie = Movie(name, link=link)
                if self.is_in_all_time_movies(movie):
                    movie = self.all_time_movies[self.all_time_movies_names.index(movie.name)]
                    self.add_to_all_time_movies(movie)
                else:
                    movie = self.get_movie_data(movie, self.get_webpage(link))
                movies_list.append(movie)
        return movies_list

    # Gets the awards from the actor page
    def get_actor_data(self,soup):
        awards = []
        #This ul class will probably change in the future as the website changes and will need to be updated
        awards_button_ul = soup.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers sc-46b64329-0 kzmHvV baseAlt")
        awards_button_li = awards_button_ul.find_all('li')[1]
        link = 'https://www.imdb.com'+ awards_button_li.find_all('a',href=True)[0]['href']
        
        awards_soup = self.get_webpage(link)
        #This div class will probably change in the future as the website changes and will need to be updated
        awards_div = awards_soup.find('div', 'sc-243fb82e-2 kwKkbX ipc-page-grid__item ipc-page-grid__item--span-2')
        for row in awards_div.find_all('section'):
            if row is not None and row.find('a', 'ipc-title-link-wrapper') is not None:
                award = row.find('a', 'ipc-title-link-wrapper').find(text=True).replace("\n", "")
                awards.append(award)
        return awards

    # Gets the movie year and rating from the movie page as the website changes and will need to be updated
    def get_movie_data(self,movie, soup):
        year = ''
        rating = ''
        #This ul class will probably change in the future
        year_ul = soup.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt")
        if year_ul is not None:
            year_li = year_ul.find_all('li')
            # In order to get the years which can be in the first or second positions
            if year_li[0].find('a') is not None:
                # In order to get the years which are like '2015-2016'
                try:
                    if int(year_li[0].find('a').find(text=True)) > 1900:
                        year = year_li[0].find('a').find(text=True).replace("\n", "")
                except:
                    year = year_li[0].find('a').find(text=True).replace("\n", "")
            elif len(year_li) > 1 and year_li[1].find('a') is not None:
                year = year_li[1].find('a').find(text=True).replace("\n", "")
            else:
                year = ''
        #This div class will probably change in the future as the website changes and will need to be updated
        rating_div = soup.find('div', class_="sc-bde20123-2 gYgHoj")
        if rating_div is not None:
            #This span class will probably change in the future as the website changes and will need to be updated
            rating = rating_div.find('span', 'sc-bde20123-1 iZlgcd').find(text=True).replace("\n", "")
        movie.year = year
        movie.rating = rating
        return movie

    # Reads a json file and returns the data
    def read_saved_file(self,file_name):
        with open(file_name, "r") as read_file:
            data = json.load(read_file)
        return data

    # Receives the json file and returns a list of Actor objects
    def from_json_to_objects(self,data):
        actors_list = []
        for actor in data:
            movies = []
            for movie in actor['allTimeMovies']:
                genres = []
                for genre in movie['genres']:
                    genres.append(genre)
                movie_object = Movie(movie['name'], movie['year'],movie['rating'], genres, movie['link'])
                movies.append(movie_object)
            actor_object = Actor(actor['name'], actor['about'], actor['link'], movies, actor['awards'], actor['genres'])
            actors_list.append(actor_object)
        return actors_list

    # Utilizes the selenium library to get the genres from the movie page as they are loaded dynamically
    def get_genres(self,link):
        driver = webdriver.Safari()
        driver.get(link)
        # Some pages have the genre in different spots so we scroll to near where they are loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        genres_list = []
        storyline_li = soup.find('li', attrs={'data-testid': 'storyline-genres'})
        if storyline_li is not None:
            storyline_ul = storyline_li.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base")
            for row in storyline_ul.find_all('li'):
                genres_list.append(row.find('a').find(text=True).replace("\n", ""))
        print(genres_list)
        return genres_list

    # Sets the genres for each movie in the actor's allTimeMovies list
    def set_genres(self,actors):
        for actor in actors:
            for movie in actor.allTimeMovies:
                if not movie.genres:
                    movie.genres = self.get_genres(movie.link)
            actor.getGenres()
        return actors

if __name__ == "__main__":
    scrapping = Scrapping()
    actors_list = scrapping.get_actors()
    actors_list = scrapping.set_genres(actors_list)
    with open("data.json", "w") as outfile:
        outfile.write(json.dumps(actors_list, indent=4))
    