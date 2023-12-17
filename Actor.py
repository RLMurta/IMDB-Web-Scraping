# Class containing the actor/actress name, about the actor/actress, link of page, all time movies, awards in different years, 
# movie genres, and methodes to get the average rating of movies, average rating per year and get top 5 movies
import json_fix

class Actor:
    def __init__(self, name, about, link, allTimeMovies=[], awards=[], genres=[]) -> None:
        self.name = name
        self.about = about
        self.link = link
        self.allTimeMovies = allTimeMovies
        self.awards = awards
        self.genres = genres
    
    def __str__(self) -> str:
        return f'name: {self.name}, about: {self.about}, link: {self.link}, allTimeMovies: {self.allTimeMovies}, awards: {self.awards}, genres: {self.genres}'

    def __repr__(self) -> str:
        return f'Actor(\'{self.name}\', \'{self.about}\', \'{self.link}\', {self.allTimeMovies}, {self.awards}, {self.genres})'
    
    def __json__(self):
        return self.__dict__

    # Returns the average rating of an actor/actress movies
    def getAvgRating(self):
        totalRating = 0
        if len(self.allTimeMovies) == 0:
            return 0.0
        for i in self.allTimeMovies:
            if not i.rating == '':
                totalRating += float(i.rating)
        return totalRating/len(self.allTimeMovies)
    
    # Returns the average rating per year of an actor/actress
    def getAvgRatingPerYear(self):
        avgRatingPerYear = {}
        if len(self.allTimeMovies) == 0:
            return 0.0
        for i in self.allTimeMovies:
            if not i.rating == '':
                if i.year not in avgRatingPerYear:
                    avgRatingPerYear[i.year] = [float(i.rating)]
                else:
                    avgRatingPerYear[i.year].append(float(i.rating))
        for i in avgRatingPerYear:
            avgRatingPerYear[i] = sum(avgRatingPerYear[i])/len(avgRatingPerYear[i])
        return avgRatingPerYear
    
    # Returns all the genres from all the movies of an actor/actress
    def getGenres(self):
        genres = []
        if len(self.allTimeMovies) == 0:
            return 0
        for i in self.allTimeMovies:
            for j in i.genres:
                if j not in genres:
                    genres.append(j)
        self.genres = genres

    # Returns the top 5 movies of an actor/actress
    def getTop5Movies(self):
        top5 = []
        for i in self.allTimeMovies:
            if len(top5) < 5:
                top5.append(i)
            else:
                for j in top5:
                    if i.rating > j.rating:
                        top5.remove(j)
                        top5.append(i)
                        break
        return top5
