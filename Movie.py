# Class containing the movie name, year, rating, genre and link
import json_fix

class Movie:
    def __init__(self, name, year='', rating='', genres=[], link='') -> None:
        self.name = name
        self.year = year
        self.rating = rating
        self.genres = genres
        self.link = link

    def __str__(self) -> str:
        return f'name: {self.name}, year: {self.year}, rating: {self.rating}, genre: {self.genres}, link: {self.link}'

    def __repr__(self) -> str:
        return f'Movie(\'{self.name}\', \'{self.year}\', \'{self.rating}\', {self.genres}, \'{self.link}\')'
    
    def __json__(self):
        return self.__dict__
    