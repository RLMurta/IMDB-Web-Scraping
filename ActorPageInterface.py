import wx

class Interface(wx.Frame):

    def __init__(self, actor, *args, **kwargs):
        super(Interface, self).__init__(*args, **kwargs)
        self.SetTitle(actor.name)
        self.imagePanel = None
        self.SetSize((800,600))
        self.scroll = wx.ScrolledWindow(self, -1)
        self.actor = actor
        skip_size = self.create_cells()
        self.scroll.SetScrollbars(1, 1, 600, skip_size + 40)

    # Creates cells for each of the actor informations
    def create_cells(self):
        skip_size = 0
        skip_size = self.avg_rating_cells(skip_size)
        skip_size = self.create_movie_cells(skip_size)
        skip_size = self.create_awards_cells(skip_size)
        return skip_size
    
    # Creates cell for the movies ratings
    def avg_rating_cells(self, skip_size):
        skip_size += 8
        # Displays title average rating of movies
        title = wx.StaticText(self.scroll, label='Average Rating of Movies', pos=(20, skip_size))
        title_font = wx.Font(48, wx.ROMAN, wx.BOLD, wx.NORMAL)
        title.SetFont(title_font)
        skip_size += title.GetSize()[1]
        # Displays title overall average rating
        avg_rating_title = wx.StaticText(self.scroll, label='Overall Average', pos=(20, skip_size))
        avg_rating_title_font = wx.Font(32, wx.ROMAN, wx.BOLD, wx.NORMAL)
        avg_rating_title.SetFont(avg_rating_title_font)
        skip_size += avg_rating_title.GetSize()[1]
        # Displays average rating
        avg_rating = self.actor.getAvgRating()
        avg_rating = wx.StaticText(self.scroll, label=f'{round(avg_rating,2)}', pos=(20, skip_size))
        avg_rating_font = wx.Font(24, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        avg_rating.SetFont(avg_rating_font)
        skip_size += avg_rating.GetSize()[1]
        # Displays title average rating per year
        avg_rating_per_year_title = wx.StaticText(self.scroll, label='Per Year', pos=(20, skip_size))
        avg_rating_per_year_title_font = wx.Font(32, wx.ROMAN, wx.BOLD, wx.NORMAL)
        avg_rating_per_year_title.SetFont(avg_rating_per_year_title_font)
        skip_size += avg_rating_per_year_title.GetSize()[1]
        # Displays average rating per year
        avg_rating_per_year = self.actor.getAvgRatingPerYear()
        for i in avg_rating_per_year:
            rating = wx.StaticText(self.scroll, label=f'({i}) - {round(avg_rating_per_year[i],2)}', pos=(20, skip_size))
            rating_font = wx.Font(24, wx.ROMAN, wx.NORMAL, wx.NORMAL)
            rating.SetFont(rating_font)
            skip_size += rating.GetSize()[1] + 20
        return skip_size

    # Creates cell for the actor's movies
    def create_movie_cells(self, skip_size):
        skip_size += 8
        # Displays title movies
        title = wx.StaticText(self.scroll, label='Movies', pos=(20, skip_size))
        title_font = wx.Font(48, wx.ROMAN, wx.BOLD, wx.NORMAL)
        title.SetFont(title_font)
        skip_size += title.GetSize()[1]
        # Displays title top 5 movies
        top5_movies = wx.StaticText(self.scroll, label='Top 5 Movies', pos=(20, skip_size))
        top5_movies_font = wx.Font(32, wx.ROMAN, wx.BOLD, wx.NORMAL)
        top5_movies.SetFont(top5_movies_font)
        skip_size += top5_movies.GetSize()[1]
        # Displays top 5 movies
        top5_movies = self.actor.getTop5Movies()
        for i in top5_movies:
            movies = wx.StaticText(self.scroll, label=f'({i.year}) - {i.name}\nGenres: {i.genres}', pos=(20, skip_size))
            movies_font = wx.Font(24, wx.ROMAN, wx.NORMAL, wx.NORMAL)
            movies.SetFont(movies_font)
            movies.Wrap(700)
            skip_size += movies.GetSize()[1] + 20
        # Displays title all time movies
        all_time_movies_title = wx.StaticText(self.scroll, label='All time Movies', pos=(20, skip_size))
        all_time_movies_title_font = wx.Font(32, wx.ROMAN, wx.BOLD, wx.NORMAL)
        all_time_movies_title.SetFont(all_time_movies_title_font)
        skip_size += all_time_movies_title.GetSize()[1]
        # Displays all time movies
        for i in self.actor.allTimeMovies:
            movies = wx.StaticText(self.scroll, label=f'({i.year}) - {i.name}', pos=(20, skip_size))
            movies_font = wx.Font(24, wx.ROMAN, wx.NORMAL, wx.NORMAL)
            movies.SetFont(movies_font)
            skip_size += movies.GetSize()[1] + 20
        return skip_size
    
    # Creates cell for the actor's awards
    def create_awards_cells(self, skip_size):
        skip_size += 8
        # Displays title awards
        title = wx.StaticText(self.scroll, label='Awards', pos=(20, skip_size))
        title_font = wx.Font(48, wx.ROMAN, wx.BOLD, wx.NORMAL)
        title.SetFont(title_font)
        skip_size += title.GetSize()[1]
        # Displays all time awards
        for i in self.actor.awards:
            award = wx.StaticText(self.scroll, label=f'{i}', pos=(20, skip_size))
            award_font = wx.Font(24, wx.ROMAN, wx.NORMAL, wx.NORMAL)
            award.SetFont(award_font)
            skip_size += award.GetSize()[1] + 20
        return skip_size
            
    
        