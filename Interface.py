import wx
import Scrapping
import ActorPageInterface

class Interface(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Interface, self).__init__(*args, **kwargs)
        self.SetTitle('IMDB')
        self.imagePanel = None
        self.SetSize((800,600))
        self.scroll = wx.ScrolledWindow(self, -1)
        scrapping = Scrapping.Scrapping()
        self.data = scrapping.from_json_to_objects(scrapping.read_saved_file('data.json'))
        cells_size = self.create_cells()
        self.scroll.SetScrollbars(1, 1, 600, cells_size + 40)

    # Creates cells for each actor
    def create_cells(self):
        skip_size = 0
        pos = 0
        for i in self.data:
            #Displays actor name
            title = wx.StaticText(self.scroll, label=i.name, pos=(20, skip_size + 20))
            title.Wrap(600)
            title_font = wx.Font(28, wx.ROMAN, wx.BOLD, wx.NORMAL)
            title.SetFont(title_font)
            skip_size += title.GetSize()[1] + 8
            # Displays about actor and genres
            about_actor = wx.StaticText(self.scroll, label=f'{i.about}\nGenres: {i.genres}', pos=(28, skip_size))
            about_actor.Wrap(600)
            about_actor_font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.NORMAL)
            about_actor.SetFont(about_actor_font)
            skip_size += about_actor.GetSize()[1] + 8
            #Displays the button that sends the user to the actor page
            more_info_bt = wx.Button(self.scroll, pos, label='More Info', pos=(28, skip_size))
            more_info_bt.Bind(wx.EVT_BUTTON, self.OnClicked, id=pos)
            skip_size += more_info_bt.GetSize()[1]
            pos += 1
        return skip_size

    # Treats the action of clicking on the button
    def OnClicked(self, event):
        ActorPageInterface.Interface(self.data[event.GetId()], None, style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)).Show()

